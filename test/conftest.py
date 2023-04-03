from pathlib import Path
from shutil import rmtree

import pytest
from faker import Faker
from sqlalchemy import create_engine

from timerdo.database import Connection
from timerdo.models import Base, Status, Timer, ToDoItem

fake = Faker()


@pytest.fixture(scope='function')
def tconnection():
    engine = create_engine('sqlite://', echo=True)
    Base.metadata.create_all(engine)
    yield Connection(engine)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def fake_todo_item():
    return ToDoItem(
        task=fake.sentence(), tag=fake.word(), deadline=fake.date_between()
    )


@pytest.fixture(scope='function')
def add_task(tconnection, fake_todo_item):
    return tconnection.add(fake_todo_item)


@pytest.fixture(scope='function')
def done_task(tconnection, add_task):
    item = tconnection.get_id(ToDoItem, 1)
    item.status = Status.done
    return tconnection.add(item)


@pytest.fixture(scope='function')
def running_timer(tconnection, add_task):
    return tconnection.add(Timer(task_id=1))


@pytest.fixture(scope='function')
def delete_test():
    rmtree(Path('./TimerdoTest'))
