import os
import time
from datetime import datetime, timedelta, date
from pathlib import Path

import typer
from sqlalchemy.exc import NoResultFound, OperationalError
from sqlmodel import Session, create_engine, select, or_
from tabulate import tabulate

from .database import ToDo, Timer, create_db_and_tables
from .functions_aux import round_timedelta, Status, make_table_view

app = typer.Typer()

APP_NAME = 'timerdo'
app_dir = typer.get_app_dir(APP_NAME)
app_dir_path = Path(app_dir)
app_dir_path.mkdir(parents=True, exist_ok=True)

sqlite_file_name = os.path.join(app_dir, 'timerdo_db.db')

sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=False)


@app.command()
def add(task: str, project: str = None, due_date: datetime = typer.Option(
    None, formats=['%Y-%m-%d']), reminder: datetime = typer.Option(
    None, formats=['%Y-%m-%d']),
        status: Status = typer.Option(Status.to_do),
        tag: str = None):
    """Add task to the to-do list."""
    try:
        today = datetime.today()

        if due_date is not None and due_date <= today:
            typer.secho(f'\ndue date must be grater than {today.date()}\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        if reminder is not None and reminder <= today:
            typer.secho(f'\nreminder must be grater than {today.date()}\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        if due_date is not None and reminder is not None and \
                reminder >= due_date:
            typer.secho(f'\nreminder must be smaller than {due_date.date()}\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        with Session(engine) as session:
            if project is not None:
                new_project = session.exec(select(ToDo).where(
                    ToDo.project == project)).first()
                if new_project is not None:
                    ongoing_project = session.exec(select(ToDo).where(
                        ToDo.project == project,
                        ToDo.status != 'done')).first()
                    if ongoing_project is None:
                        typer.secho(f'\nTasks already done in the project\n',
                                    fg=typer.colors.RED)
                        raise typer.Exit(code=1)

            new_entry = ToDo(task=task, project=project,
                             due_date=due_date, reminder=reminder,
                             status=status, tag=tag)
            session.add(new_entry)
            session.commit()
    except OperationalError:
        create_db_and_tables(engine)
        add(task=task, project=project, due_date=due_date, reminder=reminder,
            status=status, tag=tag)


@app.command()
def start(task_id: int, end: datetime = typer.Option(None,
                                                     formats=
                                                     ['%Y-%m-%d %H:%M:%S'])):
    """Start Timer for a given open task."""
    with Session(engine) as session:
        try:
            session.exec(select(Timer).where(Timer.end == None)).one()
            typer.secho('\nThe Timer must be stopped first\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)
        except NoResultFound:
            pass

        try:
            query = session.exec(select(ToDo).where(ToDo.id == task_id)).one()
            if not query.status == 'done':
                if query.status == 'to do':
                    query.status = 'doing'
                    session.add(query)
                session.add(Timer(id_todo=task_id))
                session.commit()
                if end is not None:
                    total_seconds = int(
                        (end - datetime.now()).total_seconds())
                    with typer.progressbar(length=total_seconds) as progress:
                        while datetime.now() < end:
                            time.sleep(1)
                            progress.update(1)
                        else:
                            typer.secho('\nYou Time is over! Well done!\n',
                                        blink=True,
                                        fg=typer.colors.BRIGHT_GREEN)
                            stop()
            else:
                typer.secho(f'\nTask already done\n',
                            fg=typer.colors.RED)
                raise typer.Exit(code=1)

        except NoResultFound:
            typer.secho(f'\nInvalid task id\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def stop(remarks: str = None):
    """Stop Timer."""
    with Session(engine) as session:
        try:
            query_timer = session.exec(
                select(Timer).where(Timer.end == None)).one()
            query_timer.end = datetime.now()
            query_timer.duration = query_timer.end - query_timer.start
            session.add(query_timer)

            query = session.exec(
                select(ToDo).where(ToDo.id == query_timer.id_todo)).one()

            check = typer.confirm('Is the task done?')

            if not check and not remarks:
                pass
            else:
                if check:
                    query.status = 'done'
                    query.data_end = query_timer.end.date()
                if remarks:
                    query.remarks = remarks

            session.add(query)
            session.commit()

        except NoResultFound:
            typer.secho(f'No task running', fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def view(due_date: datetime = typer.Option(None, formats=['%Y-%m-%d'])):
    """View to-do list"""
    overdue = select(ToDo).where(ToDo.due_date < date.today(),
                                 ToDo.status != 'done').order_by(ToDo.due_date)

    reminders = select(ToDo).where(ToDo.reminder == date.today(),
                                   ToDo.status != 'done').order_by(
        ToDo.due_date)

    if due_date is None:
        due_date = date.today() + timedelta(weeks=1)

    due_in = select(ToDo).where(
        ToDo.due_date < due_date, ToDo.due_date >= date.today(),
        ToDo.status != 'done').order_by(ToDo.due_date)

    no_due = select(ToDo).where(
        ToDo.due_date == None, ToDo.status != 'done',
        ToDo.reminder == None).order_by(ToDo.date_init)

    if len(make_table_view(engine, overdue)) > 1:
        typer.secho(f'\nOVERDUE\n', fg=typer.colors.BRIGHT_RED,
                    bold=True)
        typer.secho(tabulate(make_table_view(engine, overdue),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)

    if len(make_table_view(engine, reminders)) > 1:
        typer.secho(f'\nREMINDERS\n', fg=typer.colors.BRIGHT_YELLOW, bold=True)
        typer.secho(tabulate(make_table_view(engine, reminders),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)

    if len(make_table_view(engine, due_in)) > 1:
        typer.secho(f'\nDUE IN\n', fg=typer.colors.BRIGHT_GREEN, bold=True)
        typer.secho(tabulate(make_table_view(engine, due_in),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)

    if len(make_table_view(engine, no_due)) > 1:
        typer.secho(f'\nNO DUE\n', fg=typer.colors.BRIGHT_BLUE, bold=True)
        typer.secho(tabulate(make_table_view(engine, no_due),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)
    print('\n')


def report():
    ...


def log():
    ...


def edit_todo():
    ...


def edit_timer():
    ...


def edit():
    ...
