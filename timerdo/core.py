from datetime import date, datetime
from string import capwords
from typing import NoReturn

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, UnmappedInstanceError

from .database import Connection, engine
from .exceptions import (
    DoneTaskError,
    IdNotFoundError,
    NegativeIntervalError,
    NoChangingError,
    NoTimeRunningError,
    OutOffPeriodError,
    RunningTimerError,
)
from .models import Status, Timer, ToDoItem

connection = Connection(engine)


def add_task(
    task: str,
    tag: str | None = None,
    deadline: date | None = None,
    status: Status = Status.to_do,
    session: Connection = connection,
) -> NoReturn:
    """Add a new task to the todo_list table.

    Args:
        task (str): Descriptive of the task.
        tag (str | None): A tag to be used as filter.
        deadline (date | None): A given deadline or Null.
        status (Status): to_do = 'To Do'; doing = 'Doing'; done = 'Done'.
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    if tag:
        tag = capwords(tag)

    new_task = ToDoItem(
        task=capwords(task),
        tag=tag,
        deadline=deadline,
        status=Status(status),
    )

    return session.add(new_task)


def add_timer(task_id: int, session: Session = connection) -> NoReturn:
    """Add a new timer to the timer_list table.

    Args:
        task_id (int): ToDoItem item id.
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    try:
        task = session.get_id(ToDoItem, task_id)
        if task.status == Status.done:
            raise DoneTaskError(f"Task {task_id} already done.")
        if session.execute(
            select(Timer).where(Timer.finished_at == None)  # noqa
        ).first():
            raise RunningTimerError("Timer is already running.")

        new_timer = Timer(task_id=task_id)
        task.status = Status.doing

        session.add(new_timer)
        return session.add(task)

    except AttributeError:
        raise IdNotFoundError(f"Task {task_id} does not exist.")


def finish_timer(session: Session = connection) -> NoReturn:
    """Add `finished_at` to the last timer_list table row when it is `None`.

    Args:
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    try:
        timer = session.execute(
            select(Timer).where(Timer.finished_at == None)  # noqa
        ).one()[0]

        timer = session.get_id(Timer, timer.id)
        timer.finished_at = datetime.utcnow()

        return session.add(timer)

    except NoResultFound:
        raise NoTimeRunningError("No timer running.")


def delete_item(
    id: int, model: ToDoItem | Timer, session: Session = connection
) -> NoReturn:
    """Delete a row from a given table, given an `id`.

    Args:
        task_id (int): ToDoItem item id.
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    try:
        item = session.get_id(model, id)

        return session.delete(item)
    except UnmappedInstanceError:
        raise IdNotFoundError(
            f"Item {id} from {model.__tablename__} does not exist."
        )


def edit_todo_item(
    id: int,
    task: str | None = None,
    tag: str | None = None,
    deadline: date | None = None,
    status: Status | None = None,
    session: Connection = connection,
) -> NoReturn:
    """Edit a todo item.

    Args:
        id (int): ToDoItem item id.
        task (str): Descriptive of the task.
        tag (str | None): A tag to be used as filter.
        deadline (date | None): A given deadline or Null.
        status (Status): to_do = 'To Do'; doing = 'Doing'; done = 'Done'.
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    try:
        item = session.get_id(ToDoItem, id)

        if task:
            item.task = capwords(task)
        if tag:
            item.tag = capwords(tag)
        if deadline:
            item.deadline = deadline
        if status:
            item.status = status

        return session.add(item)

    except UnmappedInstanceError:
        raise IdNotFoundError(f"Item {id} does not exist.")


def edit_timer_item(
    id: int,
    created_at: datetime | None = None,
    finished_at: datetime | None = None,
    session: Connection = connection,
) -> NoReturn:
    """Edit a timer item given an `id`.

    Args:
        id (int): Timer item id.
        created_at (datetime | None): datetime to edit.
        finished_at (datetime | None): datetime to edit.
        session (Connection): Connection object.

    Returns:
        bool: True
    """
    try:
        if session.execute(
            select(Timer).where(Timer.finished_at == None)  # noqa
        ).first():
            raise RunningTimerError("Timer is already running.")

        item = session.get_id(Timer, id)

        diff = datetime.utcnow() - datetime.now()

        match created_at, finished_at:
            case None, None:
                raise NoChangingError("Nothing to change.")
            case None, datetime():
                created_at = item.created_at
                item.finished_at = finished_at + diff
            case datetime(), None:
                finished_at = item.finished_at
                item.created_at = created_at + diff
            case datetime(), datetime():
                item.created_at = created_at + diff
                item.finished_at = finished_at + diff

        if item.created_at >= item.finished_at:
            raise NegativeIntervalError(
                "created_at is greater than finished_at"
            )

        if finished_at >= datetime.now():
            raise OutOffPeriodError("finished_at is greater than now.")

        return session.add(item)

    except AttributeError:
        raise IdNotFoundError(f"Item {id} does not exist.")


def query_with_text(
    qtext: str = 'SELECT * FROM todo_list', 
    session: Connection = connection
    ) -> list:
    """Query all rows and columns from todo_list."""
    return session.execute(text(qtext)).all()
