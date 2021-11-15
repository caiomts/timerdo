import time
from datetime import datetime, timedelta, date

import typer
from sqlalchemy.exc import NoResultFound, OperationalError
from sqlmodel import Session, select, func
from tabulate import tabulate

from . import edit
from . import reports
from .database import create_db_and_tables, engine
from .functions_aux import Status, make_table_view, pop_up_msg
from .tables import ToDo, Timer

app = typer.Typer()
app.add_typer(reports.app, name='report', help='Print customized reports.')
app.add_typer(edit.app, name='edit', help='Edit records.')


@app.command()
def add(task: str, project: str = typer.Option(None, '--project', '-p'),
        due_date: datetime = typer.Option(None, '--due-date', '-d',
                                          formats=['%Y-%m-%d']),
        reminder: datetime = typer.Option(None, '--reminder', '-r',
                                          formats=['%Y-%m-%d']),
        status: Status = typer.Option(Status.to_do, '--status', '-s'),
        tag: str = typer.Option(None, '--tag', '-t')):
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

            new_id = session.exec(select(func.max(ToDo.id))).one()
            typer.secho(f'Add {task}. Task id: {new_id}\n',
                        fg=typer.colors.GREEN)
    except OperationalError:
        create_db_and_tables()
        add(task=task, project=project, due_date=due_date, reminder=reminder,
            status=status, tag=tag)


@app.command()
def start(task_id: int, duration: int = typer.Option(None, '--duration', '-d',
                                                     help='Duration in minutes')):
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
            query = session.get(ToDo, task_id)
            if not query.status == 'done':
                if query.status == 'to do':
                    query.status = 'doing'
                    session.add(query)
                if duration is not None:
                    duration = timedelta(minutes=duration)
                    if duration <= timedelta(minutes=0):
                        typer.secho(
                            f'\nDuration must be grater than 0\n',
                            fg=typer.colors.RED)
                        raise typer.Exit(code=1)
                    total_seconds = int(duration.total_seconds())
                    session.add(Timer(id_todo=task_id))
                    session.commit()
                    new_id = session.exec(select(func.max(Timer.id))).one()
                    typer.secho(
                        f'\nTask Start task {task_id}. Timer id: {new_id}\n',
                        fg=typer.colors.GREEN)
                    with typer.progressbar(length=total_seconds) as progress:
                        end = datetime.utcnow() + duration
                        while datetime.utcnow() < end:
                            time.sleep(1)
                            progress.update(1)
                        else:
                            typer.secho('\n\nYour Time is over! Well done!\n',
                                        blink=True,
                                        fg=typer.colors.BRIGHT_GREEN)
                            pop_up_msg()
                            remark = typer.confirm("Any remark?")
                            if remark:
                                remark = typer.prompt('Enter your remarks.')
                            else:
                                remark = None
                            stop(remarks=remark)
                            typer.Exit()
                else:
                    session.add(Timer(id_todo=task_id))
                    session.commit()

                    new_id = session.exec(select(func.max(Timer.id))).one()
                    typer.secho(
                        f'\nStart task {task_id}. Timer id: {new_id}\n',
                        fg=typer.colors.GREEN)

            else:
                typer.secho(f'\nTask already done\n',
                            fg=typer.colors.RED)
                raise typer.Exit(code=1)

        except AttributeError:
            typer.secho(f'\nInvalid task id\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def stop(remarks: str = typer.Option(None, '--remarks', '-r')):
    """Stop Timer."""
    with Session(engine) as session:
        try:
            query_timer = session.exec(
                select(Timer).where(Timer.end == None)).one()
            query_timer.end = datetime.utcnow()
            query_timer.duration = query_timer.end - query_timer.start
            session.add(query_timer)

            query = session.get(ToDo, query_timer.id_todo)

            check = typer.confirm('Is the task done?')

            if not check and not remarks:
                pass
            else:
                if check:
                    query.status = 'done'
                    query.date_end = query_timer.end.date()
                if remarks:
                    query.remarks = remarks

            session.add(query)
            session.commit()

            new_id = session.exec(select(func.max(Timer.id))).one()
            typer.secho(
                f'\nStop task ({query.id}). Timer id: {new_id}\n',
                fg=typer.colors.GREEN)

        except NoResultFound:
            typer.secho(f'\nNo task running\n', fg=typer.colors.RED)
            raise typer.Exit(code=1)


@app.command()
def view(due_date: datetime = typer.Option(datetime.today() +
                                           timedelta(weeks=1),
                                           formats=['%Y-%m-%d'])):
    """Print to-do list view."""
    overdue = select(ToDo).where(ToDo.due_date < date.today(),
                                 ToDo.status != 'done').order_by(ToDo.due_date)

    reminders = select(ToDo).where(ToDo.reminder <= date.today(),
                                   ToDo.status != 'done').order_by(
        ToDo.due_date)

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
        typer.secho(f'\nDUE IN {due_date.date()}\n',
                    fg=typer.colors.BRIGHT_GREEN, bold=True)
        typer.secho(tabulate(make_table_view(engine, due_in),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)

    if len(make_table_view(engine, no_due)) > 1:
        typer.secho(f'\nNO DUE\n', fg=typer.colors.BRIGHT_BLUE, bold=True)
        typer.secho(tabulate(make_table_view(engine, no_due),
                             headers="firstrow"), fg=typer.colors.BRIGHT_WHITE)
    print('\n')
