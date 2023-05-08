from datetime import datetime
from enum import StrEnum
from typing import NoReturn, Optional

import typer
from rich import box, print, print_json
from rich.panel import Panel

from .__init__ import __version__
from .core import (
    add_task,
    add_timer,
    delete_item,
    edit_timer_item,
    edit_todo_item,
    finish_timer,
    list_tasks_with_time,
    print_report,
    query_with_text,
)
from .models import Status, Timer, ToDoItem

app = typer.Typer()
edit_app = typer.Typer(help="Edit task or timer entries.")

app.add_typer(edit_app, name="edit")


class Table(StrEnum):
    """Status class."""

    task = 'task'
    timer = 'timer'


@app.callback(invoke_without_command=True)
def version_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help='Print version.'
    ),
) -> NoReturn:  # noqa: D205,D400,D415
    """Timerdo is a minimalist to-do list with built-in \
timer to keep your tasks on track."""
    if ctx.invoked_subcommand is None and version is False:
        print(
            Panel(
                """
[green]Timerdo is a minimalist to-do list with built-in \
timer to keep your tasks on track.[/green]

To get started call `$ timerdo --help` or read the documentation at \
https://caiomts.github.io/timerdo/
""",
                box=box.ROUNDED,
                border_style='bold bright_black',
            )
        )
    if version is True:
        print(f"Timerdo version: {__version__}")


@app.command("task")
def new_task(
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
    add_task(task=task, tag=tag, deadline=deadline, status=status)


@app.command("start")
def start_timer(
    task_id: int = typer.Argument(..., help="task id for timing.")
) -> NoReturn:
    """Start timer."""
    add_timer(task_id=task_id)


@app.command("stop")
def stop_timer(
    done: bool = typer.Option(
        ..., '--done', '-d', prompt=True, help="Set the task to Done."
    )
) -> NoReturn:
    """Stop running timer."""
    finish_timer(done=done)


@app.command("delete")
def delete_item_from_table(
    table: Table = typer.Argument(..., help="Table containing the item."),
    id: int = typer.Argument(..., help="Item id."),
) -> NoReturn:
    """Delete item, given table and item id."""
    match table:
        case 'task':
            delete_item(id=id, model=ToDoItem)
        case 'timer':
            delete_item(id=id, model=Timer)


@app.command("report")
def report_tasks(
    status: bool = typer.Option(
        False, "--done", "-d", help="Return also tasks with Done status."
    ),
    tag: Optional[list[str]] = typer.Option(
        None, "--tag", "-t", help="Filter tags."
    ),
    init: Optional[datetime] = typer.Option(
        None,
        "--init",
        "-i",
        help="Timeframe's lower boundary.",
        formats=["%Y-%m-%d"],
    ),
    end: Optional[datetime] = typer.Option(
        None,
        "--end",
        "-e",
        help="Timeframe's upper boundary.",
        formats=["%Y-%m-%d"],
    ),
    order_by: Optional[str] = typer.Option(
        None, "--order-by", "-o", help="Column to order by."
    ),
    asc: bool = typer.Option(
        False,
        "--asc",
        "-a",
        help="If ordered by it will be in ascending order.",
    ),
) -> NoReturn:
    """Print reports."""
    print_report(
        list_tasks_with_time(
            status=status,
            tags=tag,
            init=init,
            end=end,
            order_by=order_by,
            asc=asc,
        ),
        init=init,
        end=end,
    )


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


@app.command("query")
def query_sql(
    script: str = typer.Argument(..., help="sql script.")
) -> NoReturn:
    """Query the data with sql script and return a json."""
    print_json(query_with_text(script=script))
