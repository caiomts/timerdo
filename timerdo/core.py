from string import capwords
from datetime import datetime, date

from pydantic import validate_arguments
from sqlalchemy import select
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from sqlalchemy.exc import OperationalError

from database import get_session, get_connection
from models import Timer, ToDo, Status


@validate_arguments
def add_task(
        task: str,
        tag: str | None = None,
        deadline: date | None = None,
        status: Status = Status.to_do
) -> ToDo:
    """Adds a new task to the ToDo table.

    Args:
        task (str): Descriptive of the task.
        tag (str | None): A tag to be used as filter.
        deadline (date | None): A given deadline or Null.
        status (Status): to_do = 'To Do'; doing = 'Doing'; done = 'Done'

    Returns:
        ToDo: Added item.

    Raises:
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        if tag:
            tag = capwords(tag)

        new_task = ToDo(
            task=capwords(task),
            tag=tag,
            deadline=deadline,
            status=status,
        )

        session.add(new_task)

        session.commit()
        session.refresh(new_task)

        return new_task


@validate_arguments
def del_task(task_id: int) -> ToDo:
    """Deletes a task and all its timers.

    Args:
        task_id (int): Task id.

    Returns:
        ToDo: Deleted item.

    Raises:
        RuntimeError(f'Task id: {task_id} does not exist.')
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        try:
            task = session.get(ToDo, task_id)

            session.delete(task)
            session.commit()
            session.flush()

            return task
        except UnmappedInstanceError:
            raise RuntimeError(f'Task id: {task_id} does not exist.')


@validate_arguments
def edit_task(
        task_id: int,
        task: str | None = None,
        tag: str | None = None,
        deadline: date | None = None,
        status: Status = None,
) -> ToDo:
    """Edits task.

    Args:
        task_id (int): Task id of task to be editable.
        task (str | None): Descriptive of the task to edit.
        tag (str | None): A tag to edit.
        deadline (date | None): A deadline to edit.
        status: Status to edit.

    Returns:
        ToDo: Edited item.

    Raises:
        RuntimeError(f'Task id: {task_id} does not exist.')
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        try:
            task_item = session.get(ToDo, task_id)
            if task:
                task_item.task = capwords(task)
            if tag:
                task_item.tag = capwords(tag)
            if deadline:
                task_item.deadline = deadline
            if status:
                task_item.status = status

            session.add(task_item)
            session.commit()
            session.refresh(task_item)

            return task_item

        except UnmappedInstanceError:
            raise RuntimeError(f'Task id: {task_id} does not exist.')


@validate_arguments
def start_timer(task_id: int) -> Timer:
    """Starts timer for a given task.

    Args:
        task_id (int): Task id of task.

    Returns:
        Timer: Started timer.

    Raises:
        RuntimeError(f'Task id: {task_id} already done.')
        RuntimeError('Timer is running.')
        RuntimeError(f'Task id: {task_id} does not exist.')
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        try:
            task = session.get(ToDo, task_id)
            if task.status == Status.done:
                raise RuntimeError(f'Task id: {task_id} already done.')
            if session.execute(select(Timer).where(Timer.stop == None)).one():
                raise RuntimeError('Timer is running.')

        except AttributeError:
            raise RuntimeError(f'Task id: {task_id} does not exist.')

        except NoResultFound:
            new_timer = Timer(task_id=task_id)

            session.add(new_timer)
            session.commit()
            session.refresh(new_timer)

            return new_timer


@validate_arguments
def stop_timer(status: Status = Status.doing) -> Timer:
    """Stops timer.

    Args:
        status (Status): task status. 

    Returns:
        Timer: Stopped timer.

    Raises:
        RuntimeError('Timer is not running.')
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        try:
            timer_item = session.execute(
                select(Timer).where(Timer.stop == None)
            ).one()[0]

            task_item = session.get(ToDo, timer_item.task_id)

            timer_item.stop = datetime.utcnow()
            task_item.status = status

            session.add_all([task_item, timer_item])
            session.commit()
            session.refresh(timer_item)

            return timer_item
        except NoResultFound:
            raise RuntimeError('Timer is not running.')


@validate_arguments
def del_timer(timer_id: int) -> Timer:
    """Deletes a timer.

    Args:
        timer_id (int): Timer id.

    Returns:
        Timer: Deleted item.

    Raises:
        RuntimeError(f'Task id: {task_id} does not exist.')
        ValidationError: Invalid data type.
    """
    with get_session() as session:
        try:
            timer = session.get(Timer, timer_id)

            session.delete(timer)
            session.commit()
            session.flush()

            return timer
        except UnmappedInstanceError:
            raise RuntimeError(f'Timer id: {timer_id} does not exist.')


@validate_arguments
def edit_timer(stop: datetime) -> Timer:
    """Edit a running timer item.

    Args:
        stop (datetime): Stop time.

    Returns:
         Timer: Edited timer.
    """
    utcdif = datetime.now() - datetime.utcnow()
    with get_session() as session:
        timer = session.execute(
            select(Timer).where(Timer.stop == None)
            ).one()[0]
        if timer.start >= (stop -utcdif):
            raise RuntimeError('Stop must be greater than start.')
        try:
            timer.stop = (stop - utcdif)

            session.add(timer)
            session.commit()
            session.refresh(timer)

            return timer
        except NoResultFound:
            raise RuntimeError('No Running Timer.')


@validate_arguments
def add_timer(task_id: int, start: datetime, stop: datetime) -> Timer:
    """Adds a timer item.
    # TODO: It doesn't check whether the item overlay another timeframe of not.
     
    Args:
        task_id (int): Task id of task.
        Start (datetime): Start time.
        stop (datetime): Stop time.
    
    Returns:
        Timer: new timer.
    """
    utcdif = datetime.now() - datetime.utcnow()
    if start >= stop:
            raise RuntimeError('Stop must be greater than start.')

    with get_session() as session:
        try:
            task = session.get(ToDo, task_id)
            new_timer = Timer(
                task_id=task.id, start=(start - utcdif), stop=(stop - utcdif)
                )

            session.add(new_timer)
            session.commit()
            session.refresh(new_timer)

            return new_timer

        except AttributeError:
            raise RuntimeError(f'Task id: {task_id} does not exist.')
