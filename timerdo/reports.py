from datetime import datetime, timedelta
from typing import List, Optional

import typer
from sqlmodel import Session, select, col
from tabulate import tabulate

from .database import engine
from .functions_aux import make_table_projects, make_table_view, list_query, \
    round_timedelta
from .tables import ToDo

app = typer.Typer()


@app.command()
def projects(init: datetime = typer.Option(
    datetime.today() - timedelta(weeks=2), '--init', '-i',
    formats=['%Y-%m-%d']), project: Optional[List[str]] = typer.Option(
    None, '--project', '-p', help='Flag more than one.'),
        done: bool = typer.Option(False, '--done', '-d',
                                  help='Flag to see done tasks.')):
    """Print Projects report."""
    if not project:
        project = ToDo.project != None
    else:
        project = col(ToDo.project).in_(project)

    if not done:
        done = ToDo.status != 'done'
    else:
        done = ToDo.status != None

    with Session(engine) as session:
        tasks = session.exec(select(ToDo).where(
            project, done, ToDo.date_init >= init).order_by(
            ToDo.project)).all()
        project_init = {}
        for task in tasks:
            if task.project in project_init.keys() and \
                    project_init[task.project] < task.date_init:
                pass
            else:
                project_init[task.project] = task.date_init

        for key in project_init.keys():
            query = select(ToDo).where(
                ToDo.project == key, done).order_by(ToDo.date_init)
            table, proj_time = make_table_projects(engine, query)
            typer.secho(f'\n{key.upper()} - Time in: {proj_time}\n',
                        fg=typer.colors.BRIGHT_CYAN,
                        bold=True)
            typer.secho(tabulate(table, headers="firstrow"),
                        fg=typer.colors.BRIGHT_WHITE)
        print('\n')


@app.command()
def tags(init: datetime = typer.Option(datetime.today() - timedelta(weeks=2),
                                       '--init', '-i', formats=['%Y-%m-%d']),
         tag: Optional[List[str]] = typer.Option(None, '--tag', '-t',
                                                 help='Flag more than one.'),
         done: bool = typer.Option(False, '--done', '-d',
                                   help='Flag to see done tasks.')):
    """Print tasks per tag."""
    if not tag:
        tag = ToDo.tag != None
    else:
        tag = ToDo.tag == tag

    if not done:
        done = ToDo.status != 'done'
    else:
        done = ToDo.status != None

    with Session(engine) as session:
        tasks = session.exec(select(ToDo.tag).where(
            tag, done, ToDo.date_init >= init).order_by(
            ToDo.tag).distinct()).all()
        print(tasks)

        for key in tasks:
            query = select(ToDo).where(
                ToDo.tag == key, done).order_by(ToDo.date_init)
            table = make_table_view(engine, query)
            typer.secho(f'\n{key.upper()}\n',
                        fg=typer.colors.BRIGHT_CYAN,
                        bold=True)
            typer.secho(tabulate(table, headers="firstrow"),
                        fg=typer.colors.BRIGHT_WHITE)
        print('\n')


@app.command()
def log(init: datetime = typer.Option(datetime.today() - timedelta(weeks=4),
                                      '--init', '-i', formats=['%Y-%m-%d'])):
    """Print to-do list."""
    query = select(ToDo).where(ToDo.date_init >= init)
    table = make_table_view(engine, query)
    typer.secho(f'\nTASKS FROM {init.date()} TILL NOW\n',
                fg=typer.colors.GREEN,
                bold=True)
    typer.secho(f'\n{tabulate(table, headers="firstrow")}\n',
                fg=typer.colors.BRIGHT_WHITE)


@app.command()
def task(id: int):
    """Print one task."""
    try:
        query = select(ToDo).where(ToDo.id == id)
        for i in list_query(engine, query):
            task = dict(i[0])
            duration = i[1]
        task.pop('_sa_instance_state')
        timers = task['timers']
        task.pop('timers')

        table_task = [['Start', 'End', 'Tag', 'Remarks', 'Reminder'],
                      [task['date_init'], task['date_end'], task['tag'],
                       task['remarks'], task['reminder']]]

        typer.secho(f"""
{task['task']}

ID: {task['id']}                    DUE IN: {task['due_date']}  
        
STATUS: {task['status'].upper()}            PROJECT: {task['project']}
""",
                    fg=typer.colors.GREEN, bold=True)

        typer.secho(f'\n{tabulate(table_task, headers="firstrow")}\n',
                    fg=typer.colors.BRIGHT_WHITE)

        table_timer = [['id', 'Start', 'End', 'HH:MM']]
        for timer in timers:
            timer = dict(timer)
            timer.pop('_sa_instance_state')
            timer.pop('id_todo')
            values = [timer['id'], timer['start'].strftime('%Y-%m-%d %H:%M'),
                      timer['end'].strftime('%Y-%m-%d %H:%M'),
                      round_timedelta(timer['duration'])]
            table_timer.append(values)

        typer.secho(f"""
TIME TABLE ({round_timedelta(duration)})
""", fg=typer.colors.GREEN, bold=True)

        typer.secho(f'\n{tabulate(table_timer, headers="firstrow")}\n',
                    fg=typer.colors.BRIGHT_WHITE)

    except AttributeError:
        typer.secho(f'\nInvalid task id\n',
                    fg=typer.colors.RED)
        raise typer.Exit(code=1)
