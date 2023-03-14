from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from timerdo.models import Base, ToDo

fake = Faker()


@pytest.fixture(scope='function')
def connection():
    engine = create_engine('sqlite://', echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def fake_task():
    yield fake.sentence(nb_words=5)


@pytest.fixture(scope='function')
def fake_overdue_date():
    yield fake.date_between()


@pytest.fixture(scope='function')
def fake_todo_item(fake_task, connection):
    with connection.begin() as session:
        session.add(ToDo(task=fake_task))

