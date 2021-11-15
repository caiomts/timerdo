from datetime import datetime
from typing import Optional

import typer
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import Session, select

from .database import engine
from .functions_aux import Status
from .tables import ToDo, Timer

app = typer.Typer()


@app.command()
def task(id: str, task: str = None,
         status: Optional[Status] = typer.Option(None),
         tag: str = None, remarks: str = None, project: str = None,
         due_date: datetime = typer.Option(None, formats=['%Y-%m-%d']),
         reminder: datetime = typer.Option(None, formats=['%Y-%m-%d'])):
    """Edit record from to-do list"""
    with Session(engine) as session:
        try:
            query = session.get(ToDo, id)

            if task is not None:
                query.task = task
            if tag is not None:
                query.tag = tag
            if remarks is not None:
                query.remarks = remarks
            if project is not None:
                query.project = project

            if status is None or status == query.status:
                pass
            elif status == 'done':
                query.status = status
                query.date_end = datetime.now().date()
            elif status == 'doing' and query.status == 'done':
                query.status = status
                query.date_end = None
            elif status == 'to do':
                timer = session.exec(select(Timer).where(
                    Timer.id_todo == id)).all()
                if len(timer) > 0:
                    typer.secho(f'\nTask already started\n',
                                fg=typer.colors.RED)
                    raise typer.Exit(code=1)
                else:
                    query.status = status
                    query.date_end = None
            else:
                query.status = status

            today = datetime.today()
            if due_date is not None and reminder \
                    is not None and reminder >= due_date:
                typer.secho(
                    f'\nreminder must be smaller than {due_date.date()}\n',
                    fg=typer.colors.RED)
                raise typer.Exit(code=1)

            elif due_date is not None and due_date <= today:
                typer.secho(f'\ndue date must be grater than {today.date()}\n',
                            fg=typer.colors.RED)
                raise typer.Exit(code=1)

            elif reminder is not None and reminder <= today:
                typer.secho(
                    f'\nreminder must be grater than {today.date()}\n',
                    fg=typer.colors.RED)
                raise typer.Exit(code=1)

            elif due_date is not None and query.reminder \
                    is not None and due_date < query.reminder:
                typer.secho(
                    f'\ndue date must be grater than {query.reminder.date()}\n',
                    fg=typer.colors.RED)
                raise typer.Exit(code=1)

            elif reminder is not None and query.due_date \
                    is not None and reminder >= query.due_date:
                typer.secho(
                    f'\nreminder must be smaller than {query.due_date.date()}\n',
                    fg=typer.colors.RED)
                raise typer.Exit(code=1)

            elif reminder is not None:
                query.reminder = reminder
            elif due_date is not None:
                query.due_date = due_date

            session.add(query)
            edit = typer.confirm(f"""Are you sure you want to edit:
                {query}""")
            if not edit:
                typer.secho("Not editing",
                            fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho("Editing it!",
                        fg=typer.colors.RED)
            session.commit()
        except AttributeError:
            typer.secho(f'\nInvalid task id\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)
        except UnmappedInstanceError:
            typer.secho(f'\nInvalid task id\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def project(project: str, new_project: str):
    """Edit project name in tasks"""
    with Session(engine) as session:
        tasks = session.exec(select(ToDo).where(
            ToDo.project == project)).all()
        if len(tasks) > 0:
            for task in tasks:
                task.project = new_project
                session.add(task)
            edit = typer.confirm(f"""Are you sure you want to edit:
            {tasks}""")
            if not edit:
                typer.secho("Not editing",
                            fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho("Editing it!",
                        fg=typer.colors.RED)
            session.commit()
        else:
            typer.secho(f'\nInvalid project\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def del_task(id: str):
    """Delete task"""
    try:
        with Session(engine) as session:
            task = session.get(ToDo, id)
            timers = session.exec(select(Timer).where(
                Timer.id_todo == task.id)).all()
            for timer in timers:
                session.delete(timer)
            session.delete(task)
            edit = typer.confirm(f"""Are you sure you want to delete:
            {task}""")
            if not edit:
                typer.secho("Not deleting",
                            fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho("Deleting it!",
                        fg=typer.colors.RED)
            session.commit()
    except UnmappedInstanceError:
        typer.secho(f'\nInvalid task id\n',
                    fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def del_project(project: str):
    """Delete all tasks from a project"""
    with Session(engine) as session:
        tasks = session.exec(select(ToDo).where(
            ToDo.project == project)).all()
        if len(tasks) > 0:
            for task in tasks:
                timers = session.exec(select(Timer).where(
                    Timer.id_todo == task.id)).all()
                for timer in timers:
                    session.delete(timer)
                session.delete(task)
                session.delete(task)
            edit = typer.confirm(f"""Are you sure you want to delete:
            {tasks}""")
            if not edit:
                typer.secho("Not deleting",
                            fg=typer.colors.RED)
                raise typer.Abort()
            typer.secho("deleting it!",
                        fg=typer.colors.RED)
            session.commit()
        else:
            typer.secho(f'\nInvalid project\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)
