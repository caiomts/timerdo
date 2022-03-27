import os
import random
from datetime import datetime, timedelta

from faker import Faker
from run_before_tests import before
from sqlmodel import Session, select

from timerdo.aux import Status
from timerdo.database import create_db_and_tables, engine, sqlite_file_name
from timerdo.main import app
from timerdo.tables import Timer, ToDo


def fake_task():
    task = Faker().sentence(nb_words=8)
    return task


def fake_project():
    return Faker().sentence(nb_words=2)


def fake_tag():
    return Faker().word()


def date_before_today():
    return Faker().date_between().strftime('%Y-%m-%d')


def date_after_today(start=3, end=50):
    return (
        Faker()
        .date_between_dates(
            date_start=datetime.today() + timedelta(days=start),
            date_end=datetime.today() + timedelta(days=end),
        )
        .strftime('%Y-%m-%d')
    )


def date_before_due_date(date_after_today):
    due_date = datetime.strptime(date_after_today, '%Y-%m-%d').date()
    return (due_date - timedelta(1)).strftime('%Y-%m-%d')


list_status = random.choices([Status.doing, Status.to_do, Status.done], k=3)


def add_overdue_task(list_status=list_status):
    for status in list_status:
        task = fake_task()
        project = fake_project()
        tag = fake_tag()
        due_date = date_before_today()
        reminder = date_before_due_date(due_date)
        if status == Status.done:
            date_end = date_after_today(start=6, end=15)
        else:
            date_end = None
        with Session(engine) as session:
            task = ToDo(
                task=task,
                status=status,
                project=project,
                tag=tag,
                due_date=due_date,
                reminder=reminder,
                date_end=date_end,
            )
            session.add(task)
            session.commit()


def add_reminders_task(list_status=list_status):
    for status in list_status:
        task = fake_task()
        project = fake_project()
        tag = fake_tag()
        due_date = date_after_today(start=0, end=6)
        reminder = date_before_due_date(due_date)
        if status == Status.done:
            date_end = date_after_today(start=6, end=15)
        else:
            date_end = None
        with Session(engine) as session:
            task = ToDo(
                task=task,
                status=status,
                project=project,
                tag=tag,
                due_date=due_date,
                reminder=reminder,
                date_end=date_end,
            )
            session.add(task)
            session.commit()


def add_due_in_task(list_status=list_status):
    for status in list_status:
        task = fake_task()
        project = fake_project()
        tag = fake_tag()
        due_date = date_after_today(start=0, end=5)
        reminder = date_before_due_date(due_date)
        if status == Status.done:
            date_end = date_after_today(start=6, end=15)
        else:
            date_end = None
        with Session(engine) as session:
            task = ToDo(
                task=task,
                status=status,
                project=project,
                tag=tag,
                due_date=due_date,
                reminder=reminder,
                date_end=date_end,
            )
            session.add(task)
            session.commit()


def add_no_due_date_task(list_status=list_status):
    for status in list_status:
        task = fake_task()
        project = fake_project()
        tag = fake_tag()
        if status == Status.done:
            date_end = date_after_today(start=6, end=15)
        else:
            date_end = None
        with Session(engine) as session:
            task = ToDo(
                task=task,
                status=status,
                project=project,
                tag=tag,
                date_end=date_end,
            )
            session.add(task)
            session.commit()


def add_timer(list_status=list_status):
    max_id = 4 * (len(list_status) + 1)
    for number in range(100):
        with Session(engine) as session:
            timer = Timer(
                id_todo=random.randrange(max_id),
                end=datetime.utcnow()
                + timedelta(minutes=(random.randrange(200))),
            )
            session.add(timer)
            session.commit()


if __name__ == '__main__':
    before()

    if not os.path.isfile(sqlite_file_name):
        create_db_and_tables()

    add_overdue_task()
    add_due_in_task()
    add_reminders_task()
    add_no_due_date_task()
    add_timer()
