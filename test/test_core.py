import pytest
from timerdo.core import (
    add_session, get_session, add_task, add_timer, finish_timer
)
from timerdo.models import ToDo, Timer


def test_add_session(connection, fake_task):
    assert add_session(ToDo(task=fake_task), connection) == None
    assert add_session(Timer(task_id=1), connection) == None


def test_get_session(connection, fake_todo_item):
    assert type(get_session(ToDo, 1, connection)) is ToDo


def test_add_task_without_task(connection):
    with pytest.raises(TypeError):
        add_task(session=connection)


def test_add_task(connection, fake_task):
    assert add_task(task=fake_task, session=connection) == True


def test_add_finish_timer(connection, fake_todo_item):
    assert add_timer(task_id=1, session=connection) == True
    assert get_session(ToDo, 1, connection).status == 'Doing'
    assert finish_timer(connection) == True




