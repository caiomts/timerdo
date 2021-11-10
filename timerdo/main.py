import os
from datetime import datetime, timedelta, date
from pathlib import Path

import typer
from sqlalchemy.exc import NoResultFound, OperationalError
from sqlmodel import Session, create_engine, select

from .build_db import Project, ToDo, Timer, create_db_and_tables

app = typer.Typer()

APP_NAME = 'timerdo'
app_dir = typer.get_app_dir(APP_NAME)
app_dir_path = Path(app_dir)
app_dir_path.mkdir(parents=True, exist_ok=True)

sqlite_file_name = os.path.join(app_dir, 'timerdo_db.db')

sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=False)


@app.command()
def add(task: str, project: str = None, due_date: datetime = None,
        reminder: datetime = None,
        status: str = typer.Option('to do', help='[to do|doing]'),
        tag: str = None):
    """Add task to the to-do list."""
    try:
        if status not in ['to do', 'doing']:
            typer.echo(typer.style('status must be "to do" or "doing"',
                                   fg=typer.colors.RED))
            raise typer.Exit(code=1)

        today = date.today()

        if due_date is not None and due_date <= today:
            typer.secho(f'due date must be grater than {today}',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        if reminder is not None and reminder <= today:
            typer.secho(f'reminder must be grater than {today}',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        if due_date is not None and reminder is not None and \
                reminder >= due_date:
            typer.secho(f'reminder must be smaller than {due_date.date()}',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)

        with Session(engine) as session:
            if project is not None:
                if session.exec(select(
                        Project).where(Project.name ==
                                       project)).one_or_none() is None:
                    project = Project(name=project, date_init=date.today())
                else:
                    project = session.exec(select(
                        Project).where(Project.name ==
                                       project)).one()

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
def start(task_id: int):
    """Start Timer for a given open task (status equal "to do" or "doing")."""
    with Session(engine) as session:
        try:
            session.exec(select(Timer).where(Timer.end == None)).one()
            typer.secho('The Timer must be stopped first',
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
            else:
                typer.secho(f'Task already done',
                            fg=typer.colors.RED)
                raise typer.Exit(code=1)

        except NoResultFound:
            typer.secho(f'Invalid task id',
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

            query_duration = session.exec(
                select(Timer.duration).where(
                    Timer.id_todo == query_timer.id_todo)
            ).all()

            query = session.exec(
                select(ToDo).where(ToDo.id == query_timer.id_todo)).one()

            query.duration = sum(query_duration, timedelta(0))

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


def view():
    ...


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
