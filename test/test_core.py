from datetime import datetime, timedelta
from string import capwords

import pytest
from faker import Faker
from sqlalchemy import text

from timerdo.core import (
    add_task,
    add_timer,
    delete_item,
    edit_timer_item,
    edit_todo_item,
    finish_timer,
    query_with_text,
)
from timerdo.models import Status, Timer, ToDoItem


def test_connection_add(tconnection, fake_todo_item):
    tconnection.add(fake_todo_item)
    assert tconnection.get_id(ToDoItem, 1).status == Status.to_do


def test_connection_delete(tconnection, add_task):
    item = tconnection.get_id(ToDoItem, 1)
    tconnection.delete(item)
    assert tconnection.get_id(ToDoItem, 1) is None


def test_connection_execute(tconnection, add_task):
    assert (
        tconnection.execute(text('SELECT * FROM todo_list')).one().status
        == Status.to_do
    )


def test_add_task_without_task(tconnection):
    with pytest.raises(SystemExit) as e:
        add_task(session=tconnection)
        assert e.value.code == 1


def test_add_task(tconnection, fake_todo_item):
    task = fake_todo_item.task
    tag = fake_todo_item.tag
    deadline = fake_todo_item.deadline
    add_task(task=task, tag=tag, deadline=deadline, session=tconnection)
    item = tconnection.get_id(ToDoItem, 1)
    assert item.task == capwords(task)
    assert item.tag == capwords(tag)
    assert item.deadline == deadline
    assert item.status == Status.to_do


def test_add_timer_attribute_error(tconnection):
    with pytest.raises(SystemExit) as e:
        add_timer(1, session=tconnection)
        assert e.value.code == 1


def test_add_timer(tconnection, add_task):
    add_timer(1, session=tconnection)
    assert tconnection.get_id(Timer, 1).id == 1


def test_add_timer_done_task(tconnection, done_task):
    with pytest.raises(SystemExit) as e:
        add_timer(1, session=tconnection)
        assert e.value.code == 1


def test_add_timer_running_timer(tconnection, running_timer):
    with pytest.raises(SystemExit) as e:
        add_timer(1, session=tconnection)
        assert e.value.code == 1


def test_finish_timer(tconnection, running_timer):
    finish_timer(done=False, session=tconnection)
    assert (
        tconnection.execute(
            text('SELECT * FROM timer_list WHERE finished_at = NULL')
        ).all()
        == []
    )


def test_finish_timer_no_running(tconnection):
    with pytest.raises(SystemExit) as e:
        finish_timer(done=True, session=tconnection)
        assert e.value.code == 1


def test_delete_item(tconnection, add_task):
    delete_item(1, ToDoItem, tconnection)
    assert tconnection.get_id(ToDoItem, 1) is None


def test_delete_item_wrong_id(tconnection):
    with pytest.raises(SystemExit) as e:
        delete_item(1, ToDoItem, tconnection)
        assert e.value.code == 1


def test_edit_todo_item_wrong_id(tconnection):
    with pytest.raises(SystemExit) as e:
        edit_todo_item(1, session=tconnection)
        assert e.value.code == 1


def test_edit_todo_item(tconnection, add_task):
    fake = Faker()
    task = fake.sentence()
    tag = fake.word()
    deadline = fake.date_between()

    edit_todo_item(
        1,
        task=task,
        tag=tag,
        deadline=deadline,
        status=Status.done,
        session=tconnection,
    )

    item = tconnection.get_id(ToDoItem, 1)
    assert item.task == capwords(task)
    assert item.tag == capwords(tag)
    assert item.deadline == deadline
    assert item.status == Status.done


def test_edit_timer(tconnection, running_timer):
    finish_timer(done=False, session=tconnection)

    now = datetime.now()
    finished_at = now
    created_at = now - timedelta(hours=1)

    edit_timer_item(
        1, created_at=created_at, finished_at=finished_at, session=tconnection
    )

    timer = tconnection.get_id(Timer, 1)
    assert timer.finished_at - timer.created_at == timedelta(hours=1)


def test_edit_timer_running_timer(tconnection, running_timer):
    with pytest.raises(SystemExit) as e:
        edit_timer_item(1, session=tconnection)
        assert e.value.code == 1


def test_edit_timer_no_change_timer(tconnection, running_timer):
    finish_timer(done=False, session=tconnection)
    with pytest.raises(SystemExit) as e:
        edit_timer_item(1, session=tconnection)
        assert e.value.code == 1


def test_edit_timer_no_created_at(tconnection, running_timer):
    finish_timer(done=False, session=tconnection)

    diff = datetime.utcnow() - datetime.now()
    finished_at = datetime.now()
    finished_at_utc = finished_at + diff

    edit_timer_item(1, finished_at=finished_at, session=tconnection)

    timer = tconnection.get_id(Timer, 1)
    assert timer.finished_at.second == finished_at_utc.second
    assert timer.finished_at.minute == finished_at_utc.minute
    assert timer.finished_at.hour == finished_at_utc.hour


def test_edit_timer_no_finished_at(tconnection, running_timer):
    finish_timer(done=False, session=tconnection)

    diff = datetime.utcnow() - datetime.now()
    created_at = datetime.now() - timedelta(hours=1)
    created_at_utc = created_at + diff

    edit_timer_item(1, created_at=created_at, session=tconnection)

    timer = tconnection.get_id(Timer, 1)
    assert timer.created_at.second == created_at_utc.second
    assert timer.created_at.minute == created_at_utc.minute
    assert timer.created_at.hour == created_at_utc.hour


def test_edit_timer_created_gt_finished(tconnection, running_timer):
    with pytest.raises(SystemExit) as e:
        finish_timer(done=False, session=tconnection)

        created_at = datetime.now() + timedelta(hours=1)

        edit_timer_item(1, created_at=created_at, session=tconnection)
        assert e.value.code == 1


def test_edit_timer_no_finished_gt_now(tconnection, running_timer):
    with pytest.raises(SystemExit) as e:
        finish_timer(done=False, session=tconnection)

        finished_at = datetime.now() + timedelta(hours=1)

        edit_timer_item(1, finished_at=finished_at, session=tconnection)
        assert e.value.code == 1


def test_edit_timer_wrong_id(tconnection):
    with pytest.raises(SystemExit) as e:
        edit_timer_item(2, finished_at=datetime.now(), session=tconnection)
        assert e.value.code == 1


def test_select_all(tconnection, running_timer):
    script = """SELECT * FROM todo_list"""
    result = query_with_text(script, session=tconnection)
    assert '{' in result
