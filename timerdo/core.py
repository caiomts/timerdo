from string import capwords
from datetime import datetime, date

from pydantic import validate_arguments
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from sqlalchemy.exc import OperationalError

from .database import connection
from .models import Timer, ToDo, Status


def add_session(model: ToDo | Timer, session: Session) -> None:
    """Adds new entry to a given table.
    
    Args:
        model (ToDo | Timer): Table model for inserting item.
        session (Session): SqlAlchemy Session.

    Returns:
        None: null.
    """
    with session.begin() as session:
        session.add(model)
    return None


def get_session(
    model: ToDo | Timer, id: int, session: Session
) -> None | ToDo | Timer:
    """Gets an entry from a given table and id.
    
    Args:
        model (ToDo | Timer): Table model for inserting item.
        id (int): Item id.
        session (Session): SqlAlchemy Session.

    Returns:
        None | ToDo | Timer: null or entry.
    """
    with session() as session:
        return session.get(model, id)


def add_task(
        task: str,
        tag: str | None = None,
        deadline: date | None = None,
        status: Status = Status.to_do,
        session: Session = connection,
) -> bool:
    """Adds a new task to the todo table.

    Args:
        task (str): Descriptive of the task.
        tag (str | None): A tag to be used as filter.
        deadline (date | None): A given deadline or Null.
        status (Status): to_do = 'To Do'; doing = 'Doing'; done = 'Done'
        session (Session): SqlAlchemy Session.

    Returns:
        bool: True
    """
    if tag:
        tag = capwords(tag)
    
    new_task = ToDo(
        task=capwords(task),
        tag=tag,
        deadline=deadline,
        status=Status(status),
    )

    add_session(new_task, session)

    return True


def add_timer(task_id: int, session: Session = connection) -> bool:
    """Adds a new timer to the timer table.
    
    Args:
        task_id (int): ToDo item id.
        session (Session): SqlAlchemy Session.
    
    Returns:
        bool: True
    """
    try:
        task = get_session(ToDo, task_id, session)
        if task.status == Status.done:
            raise RuntimeError(f"Task {task_id} already done.")
        if session().execute(
            select(Timer).where(Timer.finished_at == None)
        ).first():
                raise RuntimeError("Timer is already running.")
        
        new_timer = Timer(task_id=task_id)
        task.status = Status.doing

        add_session(new_timer, session)
        add_session(task, session)
    
    except AttributeError:
        raise RuntimeError(f"Task {task_id} does not exist.")
    
    return True


def finish_timer(session: Session = connection):
    """"""
    try:
        timer = session().execute(
            select(Timer).where(Timer.finished_at == None)
        ).one()

        print(timer)
        timer = get_session(Timer, timer[0].id, session)
        timer.finished_at = datetime.utcnow()

        add_session(timer, session)
    
    except NoResultFound:
        raise RuntimeError(f"No timer running.")
    
    return True


