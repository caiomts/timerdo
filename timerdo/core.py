import json
import sys
from datetime import date, datetime
from itertools import chain
from string import capwords
from typing import NoReturn

import numpy as np
import pandas as pd
from rich import box, print
from rich.console import Console
from rich.table import Table
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


def exception_handler(func):
    """Handle exceptions with a prittyprint."""

    def wrapper(*args, **kwargs):
        """Wrap decorated function."""
        try:
            result = func(*args, **kwargs)
        except Exception as ex:
            print(f"[bold red]:boom-emoji: {ex}[/bold red]")
            sys.exit(1)
        return result

    return wrapper


@exception_handler
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


@exception_handler
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


@exception_handler
def finish_timer(done: bool, session: Session = connection) -> NoReturn:
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

        if done is True:
            task_id = timer.task_id
            item = session.get_id(ToDoItem, task_id)
            item.status = Status.done
            session.add(item)

        return session.add(timer)

    except NoResultFound:
        raise NoTimeRunningError("No timer running.")


@exception_handler
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


@exception_handler
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


@exception_handler
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


@exception_handler
def query_with_text(script: str, session: Connection = connection) -> list:
    """Execute a sql script and return a json.

    Args:
        script (str): sql script to be executed.
        session (Connection): Connection object.

    Returns:
        str
    """
    query = [dict(row._mapping) for row in session.execute(text(script)).all()]

    return json.dumps(
        {
            k: [d[k] for d in query if k in d]
            for k in set(chain(*[x.keys() for x in query]))
        }
    )


@exception_handler
def list_tasks_with_time(
    status: bool = False,
    tags: list[str] | None = None,
    init: datetime | None = None,
    end: datetime | None = None,
    order_by: str | None = None,
    asc: bool = False,
    session: Connection = connection,
) -> pd.DataFrame:
    """List tasks with total time per task.

    Args:
        status (bool): whether print tasks with `Done` status.
        tags (list[str] | None): list of tags to filter.
        init (datetime | None): to set the lower timeframe limit `>=`.
        end (datetime | None): to set the upper timeframe limit `<`.
        order_by (str| None): to order by a given column name.
        asc (bool): whether order in ascending order.
        session (Connection): Connection object.

    Returns:
        pd.DataFrame
    """
    query_task = """SELECT
        to_do.id,
        to_do.task,
        to_do.tag,
        to_do.deadline,
        to_do.created_at date,
        to_do.status,
        timer.created_at,
        timer.finished_at
    FROM
        todo_list to_do
    LEFT JOIN timer_list timer ON to_do.id = timer.task_id
    """
    df = pd.read_sql(query_task, session.engine)

    if status is False:
        df = df.query('status != "Done"')
    if tags:
        df = df.loc[df['tag'].isin(tags)]

    df = df.assign(
        date=pd.to_datetime(df['date']).astype('datetime64[s]').dt.date,
        finished_at=pd.to_datetime(df['finished_at']),
        created_at=pd.to_datetime(df['created_at']),
        time=lambda df: (df['finished_at'] - df['created_at']).astype(
            'timedelta64[s]'
        ),
    )

    match init, end:
        case datetime(), None:
            df = df.loc[df['created_at'] >= init]
        case None, datetime():
            df = df.loc[df['created_at'] < end]
        case datetime(), datetime():
            if init >= end:
                raise NegativeIntervalError(
                    "created_at is greater than finished_at"
                )
            df = df.loc[(df['created_at'] < end) & (df['created_at'] >= init)]
        case _:
            pass

    df = (
        df.drop(columns=['created_at', 'finished_at'])
        .fillna('')
        .groupby(['id', 'date', 'task', 'tag', 'deadline', 'status'])
        .sum()
        .reset_index()
    )

    try:
        df = df.sort_values(by=order_by, ascending=asc)
    except KeyError:
        df = df.sort_values(by='id', ascending=asc)

    return df


@exception_handler
def print_report(
    df: pd.DataFrame,
    init: datetime | None,
    end: datetime | None,
) -> NoReturn:
    """Print to do list as report per tag.

    Args:
        df (pd.DataFrame): Dataframe with to do list and time column.
        init (datetime | None): to set the lower timeframe limit `>=`.
        end (datetime | None): to set the upper timeframe limit `<`.

    Returns:
        NoReturn
    """
    console = Console()
    if init is None:
        init = datetime(1789, 7, 14)
    if end is None:
        end = datetime.now()

    interval = f"\nfrom {str(init.date())} until {str(end.date())}\n"
    console.print(interval, justify='right')

    for tag in np.sort(df['tag'].unique()):
        subset = df.query(f'tag == "{tag}"')
        time = subset['time'].sum()
        table = Table(
            title=f":label-emoji:   {tag}   ---   {time}\n",
            box=box.ROUNDED,
            border_style='bold bright_black',
            title_style='bold',
        )

        table.add_column(
            "ID",
            justify='right',
            style='yellow',
            no_wrap=True,
            header_style='bold cyan',
        )
        table.add_column("Date", justify='right', style='cyan', no_wrap=True)
        table.add_column("Task", justify='left', style='bright_magenta')
        table.add_column(
            "Deadline", justify='right', style='cyan', no_wrap=True
        )
        table.add_column("Status", justify='left', style='yellow')
        table.add_column("Time", justify='center', style='cyan')

        for row in range(subset.shape[0]):
            table.add_row(
                str(subset.iloc[row, 0]),
                str(subset.iloc[row, 1]),
                str(subset.iloc[row, 2]),
                str(subset.iloc[row, 4]),
                str(subset.iloc[row, 5]),
                str(subset.iloc[row, 6]),
            )

        console.print(table, new_line_start=True)
