from string import capwords

from database import get_session
from models import Timer, ToDo, Status


def add_task(
        task: str, tag: str | None = None, status: Status = Status.to_do
) -> ToDo:
    """Adds a new task to the ToDo table.

    Args:
        task (str): Descriptive of the task.
        tag (str | None): A tag to be used as filter.
        status (Status): to_do = 'To Do'; doing = 'Doing'; done = 'Done'

    Returns:
        ToDo: Added item.

    Raises:
        TypeError: Missing task or unexpected keyword argument.
    """
    # TODO: enforce status
    with get_session() as session:
        new_task = ToDo(
            task=capwords(task),
            tag=tag,
            status=status,
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task


def delete_task(task_id: int) -> ToDo:
    """Deletes a task and all its timers.

    Args:
        task_id (int): Task id.

    Returns:
        ToDo: Deleted item.
    Raises:
        UnmappedInstanceError: Task does not exist.
    """
    with get_session() as session:
        task = session.get(ToDo, task_id)

        session.delete(task)
        session.commit()
        session.flush()

        return task


def edit_task(
        task_id: int,
        task: str | None = None,
        tag: str | None = None,
        status: Status | None = None,
) -> ToDo:
    """Edits task.

    Args:
        task_id (int): Task id of task to be editable.
        task (str | None): Descriptive of the task to edit.
        tag (str | None): A tag to edit.
        status: Status to edit.
    """
    with get_session() as session:
        task_item = session.get(ToDo, task_id)
        if task is not None:
            task_item.task = task
        if tag is not None:
            task_item.tag = tag
        # TODO: enforce status
        if status is not None:
            task_item.status = status

        session.add(task_item)
        session.commit()
        session.refresh(task_item)

        return task_item


# TODO: Timer start
# TODO: Timer stop
# TODO: Timer edit
# TODO: Timer delete
