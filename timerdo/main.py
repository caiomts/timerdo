from datetime import date, datetime
from typing import Optional, NoReturn
from enum import StrEnum

import typer
from rich import print

from .core import (
    connection,
    add_task,
    add_timer,
    finish_timer,
    delete_item,
    )
from .database import Connection, engine
from .models import Status, ToDoItem, Timer
from .__init__ import __version__


app = typer.Typer()


class Table(StrEnum):
    """Status class."""

    task = 'task'
    timer = 'timer'


@app.callback(invoke_without_command=True)
def version_callback(ctx: typer.Context):
    """Timerdo is a minimalist to-do list with built-in timer
    to keep your tasks on track.
    """
    if ctx.invoked_subcommand is None:
        print(f"Timerdo Version: {__version__}")


@app.command()
def task(
    task: str = typer.Argument(..., help="Task to be add to To-Do list."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Task tag."),
    deadline: Optional[datetime] = typer.Option(
        None, "--deadline", "-d", help="Task Deadline.", formats=["%Y-%m-%d"]
        ),
    status: Status = typer.Option(
        Status.to_do, "--status", "-s", help="Task Status."
        ),
    ) -> NoReturn:
    """Add a task to the To-Do list."""
    # TODO: Change Optional when "|" becomes supported.
    add_task(
        task=task, tag=tag, deadline=deadline, status=status
        )


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
    table: Table = typer.Argument(
        ..., help="Table containing the item."
        ),
    id: int = typer.Argument(..., help="Item id."),

    ) -> NoReturn:
    """Delete item, given table and item id."""
    match table:
        case 'task':
            delete_item(id=id, model=ToDoItem)
        case 'timer':
            delete_item(id=id, model=Timer)

