import os
import time
from datetime import date, datetime, timedelta

import typer
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn
from rich.prompt import Confirm
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, func, select

from . import edit, reports
from .aux import Status, View
from .database import create_db_and_tables, engine, sqlite_file_name
from .tables import Timer, ToDo

app = typer.Typer()
app.add_typer(reports.app, name='report', help='Print customized reports.')
app.add_typer(edit.app, name='edit', help='Edit records.')

console = Console(color_system='256', log_path=False)

if not os.path.isfile(sqlite_file_name):
    create_db_and_tables()


@app.command()
def add(
    task: str,
    project: str = typer.Option(None, '--project', '-p'),
    due_date: datetime = typer.Option(
        None, '--due-date', '-d', formats=['%Y-%m-%d']
    ),
    reminder: datetime = typer.Option(
        None, '--reminder', '-r', formats=['%Y-%m-%d']
    ),
    status: Status = typer.Option(Status.to_do, '--status', '-s'),
    tag: str = typer.Option(None, '--tag', '-t'),
):
    """Add new task to database."""
    today = datetime.today()

    if due_date is not None and due_date <= today:
        console.log(
            f'Due date must be grater than {today.date()}.\n', style='red'
        )
        raise typer.Exit(code=1)

    if reminder is not None and reminder <= today:
        console.log(
            f'Reminder must be grater than {today.date()}.\n', style='red'
        )
        raise typer.Exit(code=1)

    if due_date is not None and reminder is not None and reminder >= due_date:
        console.log(
            f'Reminder must be smaller than {due_date.date()}.\n',
            style='red',
        )
        raise typer.Exit(code=1)

    with Session(engine) as session:
        new_entry = ToDo(
            task=task,
            project=project,
            due_date=due_date,
            reminder=reminder,
            status=status,
            tag=tag,
        )

        session.add(new_entry)
        session.commit()

        new_id = session.exec(select(func.max(ToDo.id))).one()

        console.log(f'Added a new entry with ID {new_id}.\n', style='green')


@app.command()
def start(
    task_id: int,
    duration: int = typer.Option(
        None, '--duration', '-d', help='Duration in minutes'
    ),
):
    """Start Timer for a given open task."""
    if duration is not None and timedelta(minutes=duration) <= timedelta(
        minutes=1
    ):
        console.log('Duration must be grater than 1.\n', style='red')
        raise typer.Exit(code=1)

    with Session(engine) as session:
        try:
            session.exec(select(Timer).where(Timer.end == None)).one()
            console.log('Timer must be stopped first.\n', style='red')
            raise typer.Exit(code=1)
        except NoResultFound:
            pass

        try:
            query = session.exec(select(ToDo).where(ToDo.id == task_id)).one()
        except NoResultFound:
            console.log('Invalid task id.\n', style='red')
            raise typer.Exit(code=1)

        if query.status == 'done':
            console.log('Task already done.\n', style='red')
            raise typer.Exit(code=1)

        if query.status == 'to do':
            query.status = 'doing'
            session.add(query)

        session.add(Timer(id_todo=task_id))

        new_id = session.exec(select(func.max(Timer.id))).one()
        task = query.task
        console.log(
            f'{task} has just started. Timer id: {new_id}\n', style='green'
        )

        session.commit()

        if duration is not None:
            with Progress(
                SpinnerColumn(),
                transient=True,
                *Progress.get_default_columns(),
            ) as progress:
                task = progress.add_task('Working', total=duration * 60)
                while not progress.finished:
                    time.sleep(1)
                    progress.update(task, advance=1)
                else:
                    progress.console.rule(
                        'Your time is over! Well done!', style='green'
                    )

            status = Confirm.ask('\nIs the task done?\n')
            stop(status=status)
        typer.Exit()


@app.command()
def stop(status: bool = typer.Option(False, '-d', help='Done task')):
    """Stop a running task."""
    with Session(engine) as session:
        try:
            query_timer = session.exec(
                select(Timer).where(Timer.end == None)
            ).one()
            query_timer.end = datetime.utcnow()

            query_todo = session.get(ToDo, query_timer.id_todo)
            if status:
                query_todo.status = 'done'
                query_todo.date_end = date.today()
            else:
                status = Confirm.ask('\nIs the task done?\n')
                if status:
                    query_todo.status = 'done'
                    query_todo.date_end = date.today()
            console.log(
                f'Timer for "{query_todo.task}" has ended.\n', style='green'
            )

            session.commit()

        except NoResultFound:
            console.log('No running task.\n', style='red')
            raise typer.Exit(code=1)


@app.command()
def tasks(
    week: bool = typer.Option(False, '-w', help='week tasks'),
    max_date: datetime = typer.Option(
        None, '--date', '-d', formats=['%Y-%m-%d']
    )
):
    """List tasks."""
    date_limit = date.today()
    if week:
        date_limit = date.today() + timedelta(
            days=(7 - date.today().isocalendar()[2])
        )
    if max_date:
        date_limit = max_date.date()

    overdue = (
        select(ToDo)
        .where(ToDo.due_date < date.today(), ToDo.status != 'done')
        .order_by(ToDo.due_date)
    )

    reminders = (
        select(ToDo)
        .where(ToDo.reminder == date.today(), ToDo.status != 'done')
        .order_by(ToDo.reminder)
    )

    due_in = (
        select(ToDo)
        .where(
            ToDo.due_date <= date_limit,
            ToDo.due_date >= date.today(),
            ToDo.status != 'done',
        )
        .order_by(ToDo.due_date)
    )

    no_due = (
        select(ToDo)
        .where(
            ToDo.due_date == None, ToDo.status != 'done', ToDo.reminder == None
        )
        .order_by(ToDo.date_init)
    )

    first_weekday = date.today() - timedelta(
        days=(date.today().isocalendar()[2])
    )
    done_this_week = (
        select(ToDo)
        .where(ToDo.date_end >= first_weekday)
        .order_by(ToDo.date_end)
    )

    task_lists = []
    with Session(engine) as session:
        week_summary = session.exec(done_this_week).all()
        task_lists.append(('overdue', session.exec(overdue).all()))
        task_lists.append(('reminder', session.exec(reminders).all()))
        task_lists.append(('due_in', session.exec(due_in).all()))
        task_lists.append(('no_due', session.exec(no_due).all()))

    View(week_summary, engine).week_summary()
    for task_list in task_lists:
        if len(task_list[1]) >= 1:
            View(task_list[1], engine).plot_list(task_list[0], date_limit)
