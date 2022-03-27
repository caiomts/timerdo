import os
from datetime import datetime, timedelta

import pytest
from faker import Faker
from sqlmodel import Session, select
from typer.testing import CliRunner

from timerdo.database import engine
from timerdo.functions_aux import Status
from timerdo.main import app
from timerdo.tables import Timer, ToDo


@pytest.fixture(scope='session')
def runner():
    runner = CliRunner()
    yield runner


@pytest.fixture()
def fake_task():
    task = Faker().sentence(nb_words=10)
    yield task


@pytest.fixture(scope='class')
def fake_project():
    yield Faker().sentence(nb_words=3)


@pytest.fixture(scope='class')
def fake_tag():
    yield Faker().word()


@pytest.fixture(scope='class')
def date_before_today():
    yield Faker().date_between().strftime('%Y-%m-%d')


@pytest.fixture(scope='class')
def date_after_today():
    yield (
        Faker()
        .date_between_dates(
            date_start=datetime.today() + timedelta(days=3),
            date_end=datetime.today() + timedelta(days=50),
        )
        .strftime('%Y-%m-%d')
    )


@pytest.fixture(scope='class')
def date_before_due_date(date_after_today):
    due_date = datetime.strptime(date_after_today, '%Y-%m-%d').date()
    yield (due_date - timedelta(1)).strftime('%Y-%m-%d')
    with Session(engine) as session:
        task = session.exec(select(ToDo)).one()
        session.delete(task)
        session.commit()


@pytest.fixture()
def add_task(fake_task):
    with Session(engine) as session:
        task = ToDo(task=fake_task, status=Status.to_do)
        session.add(task)
        session.commit()
        task = session.exec(select(ToDo).where(ToDo.task == fake_task)).one()
        yield task.id


@pytest.fixture()
def start_timer(add_task):
    task_id = add_task
    with Session(engine) as session:
        session.add(Timer(id_todo=task_id))
        session.commit()
        yield task_id
        timer = session.exec(
            select(Timer).where(Timer.id_todo == task_id)
        ).one()
        session.delete(timer)
        session.commit()


@pytest.fixture()
def change_task_status(add_task):
    task_id = add_task
    with Session(engine) as session:
        task = session.get(ToDo, task_id)
        task.status = 'done'
        session.commit()
        yield task_id


class TestAdd:
    def test_add_with_no_argument(self, runner):
        result = runner.invoke(app, ['add'])
        assert result.exit_code == 2

    def test_add_task_with_due_date_before_today(
        self, runner, fake_task, date_before_today
    ):
        result = runner.invoke(
            app, ['add', fake_task, '--due-date', date_before_today]
        )

        assert result.exit_code == 1
        assert 'Due date must be grater than' in result.stdout

    def test_add_task_with_reminder_before_today(
        self, runner, fake_task, date_before_today
    ):
        result = runner.invoke(
            app, ['add', fake_task, '--reminder', date_before_today]
        )

        assert result.exit_code == 1
        assert 'Reminder must be grater than' in result.stdout

    def test_add_task_with_reminder_after_due_date(
        self, runner, fake_task, date_after_today
    ):
        result = runner.invoke(
            app,
            [
                'add',
                fake_task,
                '--reminder',
                date_after_today,
                '--due-date',
                date_after_today,
            ],
        )

        assert result.exit_code == 1
        assert 'Reminder must be smaller than' in result.stdout

    def test_add_all_features(
        self,
        runner,
        fake_task,
        date_after_today,
        date_before_due_date,
        fake_project,
        fake_tag,
    ):
        result = runner.invoke(
            app,
            [
                'add',
                fake_task,
                '--project',
                fake_project,
                '--due-date',
                date_after_today,
                '--reminder',
                date_before_due_date,
                '--tag',
                fake_tag,
            ],
        )
        with Session(engine) as session:
            query = session.exec(
                select(ToDo).where(ToDo.task == fake_task)
            ).one()
            task = query.task
            status = query.status
            project = query.project
            due_date = query.due_date
            reminder = query.reminder
            tag = query.tag

        assert result.exit_code == 0
        assert task == fake_task
        assert status == 'to do'
        assert project == fake_project
        assert due_date == datetime.fromisoformat(date_after_today).date()
        assert reminder == datetime.fromisoformat(date_before_due_date).date()
        assert 'Added new entry with ID' in result.stdout


class TestStartStop:
    def test_start_timer_with_sorter_duration(self, runner):
        result = runner.invoke(app, ['start', '1', '-d', '1'])
        assert result.exit_code == 1
        assert 'Duration must be grater than' in result.stdout

    def test_start_timer_with_running_task(self, runner, start_timer):
        id = str(start_timer)
        result = runner.invoke(app, ['start', id])
        assert result.exit_code == 1
        assert 'Timer must be stopped first' in result.stdout

    def test_start_timer_with_invalid_task_id(self, runner, add_task):
        id = str(add_task + 1)
        result = runner.invoke(app, ['start', id])
        assert result.exit_code == 1
        assert 'Invalid task id' in result.stdout

    def test_start_timer_with_done_task(self, runner, change_task_status):
        id = str(change_task_status)
        result = runner.invoke(app, ['start', id])
        assert result.exit_code == 1
        assert 'Task already done' in result.stdout

    def test_start_timer(self, runner, add_task):
        id = str(add_task)
        result = runner.invoke(app, ['start', id])
        assert result.exit_code == 0
        assert 'Timer id' in result.stdout

    def test_stop_timer(self, runner):
        result = runner.invoke(app, ['stop', '-d'])
        assert result.exit_code == 0
        assert 'Timer for' in result.stdout

    def test_stop_with_no_running_task(self, runner):
        result = runner.invoke(app, ['stop', '-d'])
        assert result.exit_code == 1
        assert 'No running task' in result.stdout
