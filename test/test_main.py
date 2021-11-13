from typer.testing import CliRunner

import os

from timerdo.main import app, sqlite_file_name
from timerdo.tables import ToDo, Timer
from sqlmodel import create_engine, Session, select
from datetime import datetime, timedelta

try:
    os.rename('/home/cmts/.config/timerdo/timerdo_db.db',
              '/home/cmts/.config/timerdo/timerdo_db_moved.db')
except FileNotFoundError:
    pass


sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=True)

runner = CliRunner()


def test_add_none():
    """Test add function with no argument"""
    result = runner.invoke(app, ['add'])

    assert result.exit_code == 2


def test_add_task():
    """Test add function with task argument"""
    task = 'test add'
    result = runner.invoke(app, ['add', task])
    with Session(engine) as session:
        query = session.exec(select(ToDo).where(ToDo.task == task)).one()
        task = query.task
        status = query.status

    assert result.exit_code == 0
    assert task == task
    assert status == 'to do'


def test_add_status():
    """Test status"""
    task = 'Test status'
    status = 'dif'
    result = runner.invoke(app, ['add', task, '--status', status])

    assert result.exit_code == 1
    assert 'status must be "to do" or "doing"\n' in result.stdout


def test_add_due_date():
    """Test due date"""
    task = 'Test due date'
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    result = runner.invoke(app, ['add', task, '--due-date', date])

    assert result.exit_code == 1
    assert f'due date must be grater than {datetime.today().date()}\n' in \
           result.stdout


def test_add_reminder():
    """Test reminder"""
    task = 'Test reminder'
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    result = runner.invoke(app, ['add', task, '--reminder', date])

    assert result.exit_code == 1
    assert f'reminder must be grater than {datetime.today().date()}\n' in \
           result.stdout


def test_add_due_date_reminder():
    """Test due-date and reminder"""
    task = 'Test due-date and reminder'
    due_date = datetime.strftime(
        datetime.now() + timedelta(days=2), '%Y-%m-%d')
    reminder = datetime.strftime(
        datetime.now() + timedelta(days=2), '%Y-%m-%d')
    result = runner.invoke(app, ['add', task, '--reminder', reminder,
                                 '--due-date', due_date])

    assert result.exit_code == 1
    assert f'reminder must be smaller than {due_date}\n' in \
           result.stdout


def test_add_full_entry():
    """Test add full task"""
    task = 'something'
    project = 'test project'
    due_date = datetime.strftime(
        datetime.now() + timedelta(days=2), '%Y-%m-%d')
    reminder = datetime.strftime(
        datetime.now() + timedelta(days=1), '%Y-%m-%d')
    status = 'doing'
    tag = 'tag'

    result = runner.invoke(app, ['add', task,
                                 '--project', project,
                                 '--due-date', due_date,
                                 '--reminder', reminder,
                                 '--status', status,
                                 '--tag', tag])

    assert result.exit_code == 0

    with Session(engine) as session:
        query = session.exec(select(ToDo).where(ToDo.task == task,
                                                ToDo.project == project,
                                                ToDo.status == status,
                                                ToDo.tag == tag)).one()
        assert query is not None


def test_start():
    """Test start"""
    todo_id = '1'
    result = runner.invoke(app, ['start', todo_id])

    assert result.exit_code == 0

    with Session(engine) as session:
        query = session.exec(select(ToDo.status).where(ToDo.id ==
                                                       todo_id)).one()

        assert query == 'doing'


def test_start_running():
    """Test start when running"""
    todo_id = '1'
    result = runner.invoke(app, ['start', todo_id])

    assert result.exit_code == 1
    assert 'The Timer must be stopped first' in result.stdout


def test_stop():
    """Test stop"""
    result = runner.invoke(app, ['stop'])

    assert result.exit_code == 0


def test_stop_no_run():
    """Test stop with no run"""
    result = runner.invoke(app, ['stop'])

    assert result.exit_code == 1


def test_duration():
    """test duration"""
    todo_id = 1
    with Session(engine) as session:
        todo = session.exec(select(ToDo.duration).where(ToDo.id ==
                                                        todo_id)).one()
        timer = session.exec(select(Timer.duration).where(Timer.id_todo
                                                          == todo_id)).one()

        assert todo is not None and todo == timer


def test_return_db():
    try:
        os.remove('/home/cmts/.config/timerdo/timerdo_db.db')
        os.rename('/home/cmts/.config/timerdo/timerdo_db_moved.db',
                  '/home/cmts/.config/timerdo/timerdo_db.db')
    except FileNotFoundError:
        pass