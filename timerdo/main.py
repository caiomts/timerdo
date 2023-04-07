from datetime import datetime
from enum import StrEnum
from typing import NoReturn, Optional

import typer
from rich import print

from .__init__ import __version__
from .core import (
    add_task,
    add_timer,
    delete_item,
    edit_timer_item,
    edit_todo_item,
    finish_timer,
    query_with_text,
)
from .models import Status, Timer, ToDoItem

app = typer.Typer()
edit_app = typer.Typer(help="Edit task or timer entries.")
query_app = typer.Typer(help="Query the data.")

app.add_typer(edit_app, name="edit")
app.add_typer(query_app, name="query")


class Table(StrEnum):
    """Status class."""

    task = 'task'
    timer = 'timer'


@app.callback(invoke_without_command=True)
def version_callback(ctx: typer.Context) -> NoReturn:  # noqa: D205,D400,D415
    """Timerdo is a minimalist to-do list with built-in timer
    to keep your tasks on track.
    """
    if ctx.invoked_subcommand is None:
        print(f"timerdo Version: {__version__}")


@app.command()
def task(
    task: str = typer.Argument(..., help="Task to be add to To-Do list."),
    tag: Optional[str] = typer.Option(None, "--tag", help="Task tag."),
    deadline: Optional[datetime] = typer.Option(
        None, "--deadline", "-d", help="Task Deadline.", formats=["%Y-%m-%d"]
    ),
    status: Status = typer.Option(
        Status.to_do, "--status", "-s", help="Task Status."
    ),
) -> NoReturn:
    """Add a task to the To-Do list."""
    # TODO: Change Optional when "|" becomes supported.
    add_task(task=task, tag=tag, deadline=deadline, status=status)


@app.command()
def start(
    task_id: int = typer.Argument(..., help="task id for timing.")
) -> NoReturn:
    """Start timer."""
    add_timer(task_id=task_id)


@app.command()
def stop() -> NoReturn:
    """Stop running timer."""
    finish_timer()


@app.command()
def delete(
    table: Table = typer.Argument(..., help="Table containing the item."),
    id: int = typer.Argument(..., help="Item id."),
) -> NoReturn:
    """Delete item, given table and item id."""
    match table:
        case 'task':
            delete_item(id=id, model=ToDoItem)
        case 'timer':
            delete_item(id=id, model=Timer)


@edit_app.command("task")
def edit_task(
    id: int = typer.Argument(..., help="Item id."),
    task: Optional['str'] = typer.Option(None, "--task", "-t", help="Task"),
    tag: Optional[str] = typer.Option(None, "--tag", help="Task tag."),
    deadline: Optional[datetime] = typer.Option(
        None, "--deadline", "-d", help="Task Deadline.", formats=["%Y-%m-%d"]
    ),
    status: Optional[Status] = typer.Option(
        None, "--status", "-s", help="Task Status."
    ),
) -> NoReturn:
    """Edit a task item."""
    edit_todo_item(id=id, task=task, tag=tag, deadline=deadline, status=status)


@edit_app.command("timer")
def edit_timer(
    id: int = typer.Argument(..., help="Item id."),
    created_at: Optional[datetime] = typer.Option(
        None,
        "--create_at",
        "-c",
        help="timer start.",
        formats=["%Y-%m-%d %H:%M:%S"],
    ),
    finished_at: Optional[datetime] = typer.Option(
        None,
        "--finished_at",
        "-f",
        help="timer stop.",
        formats=["%Y-%m-%d %H:%M:%S"],
    ),
) -> NoReturn:
    """Edit a timer item."""
    edit_timer_item(id=id, created_at=created_at, finished_at=finished_at)


@query_app.command("sql")
def query_sql(
    sql: str = typer.Argument(
        """
        SELECT td.id, task, tag, deadline, status, sum(
            strftime('%M', finished_at) - strftime('%M', tl.created_at)
            ) as time
        FROM todo_list as td
        LEFT OUTER JOIN timer_list as tl
        ON tl.task_id = td.id
        GROUP BY td.id, task, tag, deadline, status
        ORDER BY deadline ASC
        """,
        help="Item id.",
    )
) -> NoReturn:
    """Query the data with sql."""
    print(query_with_text(qtext=sql))
