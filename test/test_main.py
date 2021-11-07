from typer.testing import CliRunner
import sys

sys.path.append('../')

from timerdo.main import app
from timerdo.build_db import ToDo, Timer, create_db_and_tables
from sqlmodel import create_engine, Session, select
import os


sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=True)

runner = CliRunner()


def test_create_db():
    """Test create_db_and_tables"""
    os.remove(sqlite_file_name)
    result = create_db_and_tables()
    assert result is None

    with Session(engine) as session:
        query = session.exec(select(ToDo)).all()
        assert query is not None

        query = session.exec(select(Timer)).all()
        assert query is not None


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
    """Test status function"""
    task = 'Test status'
    status = 'dif'
    result = runner.invoke(app, ['add', task, '--status', status])

    assert result.exit_code == 1


#def main():
#    test_create_db()
#    test_add_none()
#    test_add_task()
#    test_add_status()


if __name__ == '__main__':
    test_create_db()
    test_add_none()
    test_add_task()
    test_add_status()
