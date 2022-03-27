from datetime import datetime
from typing import Optional

import typer
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import Session, select
from rich.console import Console
from rich.prompt import Confirm

from .aux import Status
from .database import engine
from .tables import Timer, ToDo

app = typer.Typer()

console = Console(color_system='256', log_path=False)


def confirm_task(query):
    """Handle task message."""
    edit = Confirm.ask(
                f"""[red]Are you sure you want to edit the following task?:
                [white]
                Date init: {query.date_init}
                Date end: {query.date_end}
                task: {query.task}
                project: {query.project}
                Status: {query.status}
                Tag: {query.tag}
                Due date: {query.due_date}
                Reminder: {query.reminder}\n
                """
            )
    if not edit:
        console.log('Not editing', style='red',)
        raise typer.Abort()
    console.log('Editing it!', style='red',)


def confirm_project(project):
    """Handle project message."""
    edit = Confirm.ask(
                f"""Are you sure you want to edit {project} name?"""
            )
    if not edit:
        console.log('Not editing', style='red',)
        raise typer.Abort()
    console.log('Editing it!', style='red',)


@app.command()
def task(
    id: int,
    task: str = None,
    status: Optional[Status] = typer.Option(None),
    tag: str = None,
    project: str = None,
    due_date: datetime = typer.Option(None, formats=['%Y-%m-%d']),
    reminder: datetime = typer.Option(None, formats=['%Y-%m-%d']),
):
    """Edit record from to-do list."""
    with Session(engine) as session:
        try:
            query = session.get(ToDo, id)

            if task is not None:
                query.task = task
            if tag is not None:
                query.tag = tag
            if project is not None:
                query.project = project

            timer = session.exec(
                    select(Timer).where(Timer.id_todo == id)
                ).all()

            match status:
                case None:
                    pass
                case 'done':
                    query.status = status
                    query.date_end = datetime.now().date()
                case 'doing':
                    if query.status == 'done':
                        query.date_end = None
                    query.status = status
                case 'to do':
                    if len(timer) > 0:
                        console.log('Task already started\n', style='red')
                        raise typer.Exit(code=1)
                    else:
                        query.status = status
                        query.date_end = None
                case _:
                    query.status = status

            today = datetime.today()

            if (
                due_date is not None
                and reminder is not None
                and reminder >= due_date
            ):
                console.log(
                    f'reminder must be smaller than {due_date.date()}\n',
                    style='red',
                )
                raise typer.Exit(code=1)
            elif (
                due_date is not None
                and query.reminder is not None
                and due_date < query.reminder
            ):
                console.log(
                    f'due date must be grater than {query.reminder.date()}\n',
                    style='red',
                )
                raise typer.Exit(code=1)
            elif (
                reminder is not None
                and query.due_date is not None
                and reminder >= query.due_date
            ):
                console.log(
                    f'reminder must be smaller than {query.due_date.date()}\n',
                    style='red',
                )
                raise typer.Exit(code=1)
            elif reminder is not None:
                query.reminder = reminder
            elif due_date is not None:
                query.due_date = due_date

            session.add(query)
            confirm_task(query, session)
            session.commit()
        except UnmappedInstanceError:
            console.log('Invalid task id\n', style='red')
            raise typer.Exit(code=1)


@app.command()
def project(project: str, new_project: str):
    """Edit project name in tasks."""
    with Session(engine) as session:
        tasks = session.exec(select(ToDo).where(ToDo.project == project)).all()
        if len(tasks) > 0:
            for task in tasks:
                task.project = new_project
                session.add(task)
            confirm_project(project)
            session.commit()
        else:
            console.log('Invalid project\n', style='red',)
            raise typer.Exit(code=1)


@app.command()
def del_task(task_id: int):
    """Delete task."""
    try:
        with Session(engine) as session:
            query = session.get(ToDo, task_id)
            timers = session.exec(
                select(Timer).where(Timer.id_todo == query.id)
            ).all()
            for timer in timers:
                session.delete(timer)
            session.delete(query)
            confirm_task(query)
            session.commit()
    except UnmappedInstanceError:
            console.log('Invalid task id\n', style='red')
            raise typer.Exit(code=1)


@app.command()
def del_project(project: str):
    """Delete all tasks from a project."""
    with Session(engine) as session:
        tasks = session.exec(select(ToDo).where(ToDo.project == project)).all()
        if len(tasks) > 0:
            for task in tasks:
                timers = session.exec(
                    select(Timer).where(Timer.id_todo == task.id)
                ).all()
                for timer in timers:
                    session.delete(timer)
                session.delete(task)
            edit = Confirm.ask(
                f"""Are you sure you want to edit {project} name?"""
            )
            if not edit:
                console.log('Not editing', style='red',)
                raise typer.Abort()
            console.log('Editing it!', style='red',)
            session.commit()
        else:
            console.log('Invalid project\n', style='red',)
            raise typer.Exit(code=1)


@app.command()
def timer(
    id: int, end: datetime = typer.Option('', formats=['%Y-%m-%d %H:%M:%S'])
):
    """Edit record from Timer"""
    with Session(engine) as session:
        try:
            query = session.get(Timer, id)
            if end <= query.start:
                typer.secho(
                    f'\nEnd must be >= {query.start}\n', fg=typer.colors.RED
                )
                raise typer.Exit(code=1)
            if end >= datetime.now():
                typer.secho(f'\nEnd must be < {datetime.now()}')
                raise typer.Exit(code=1)

            query.end = end
            session.add(query)
            edit = typer.confirm(
                f"""Are you sure you want to edit:
                        {query}"""
            )
            if not edit:
                typer.secho('Not editing', fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho('Editing it!', fg=typer.colors.RED)
            session.commit()
        except AttributeError:
            typer.secho(f'\nInvalid timer id\n', fg=typer.colors.RED)


@app.command()
def del_timer(id: int):
    """Delete record from Timer"""
    with Session(engine) as session:
        try:
            query = session.get(Timer, id)
            session.delete(query)
            edit = typer.confirm(
                f"""Are you sure you want to delete:
            {query}"""
            )
            if not edit:
                typer.secho('Not deleting', fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho('deleting it!', fg=typer.colors.RED)
            session.commit()

        except AttributeError:
            typer.secho(f'\nInvalid timer id\n', fg=typer.colors.RED)
