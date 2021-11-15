from datetime import timedelta
from enum import Enum
from tkinter import *
from tkinter import ttk
import typer

from sqlmodel import Session


class Status(str, Enum):
    """Status"""
    to_do = 'to do'
    doing = 'doing'
    done = 'done'


def round_timedelta(delta: timedelta):
    """round timedelta object"""
    seconds = round(delta.total_seconds())
    if seconds >= 3600:
        hours = round(seconds/3600)
        seconds += - hours*3600
    else:
        hours = 0
    if seconds >= 60:
        minutes = round(seconds/60)
        seconds += - minutes * 60
    else:
        minutes = 0
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)

    return f'{hours}:{minutes}'


def list_query(engine, query):
    """Calculate duration of a task"""
    with Session(engine) as session:
        query_list = session.exec(query).all()
        try:
            for task in query_list:
                duration = timedelta()
                for dur in task.timers:
                    duration += dur.duration
                yield task, duration
        except TypeError:
            typer.secho(f'\nTask is running. Stop timer first.\n',
                        fg=typer.colors.RED)
            raise typer.Exit(code=1)


def make_table_view(engine, tasks):
    table = [['id', 'Task', 'Project', 'Status', 'Tag', 'hh:mm',
              'Due in']]
    try:
        for i in list_query(engine, tasks):
            task = i[0]
            duration = i[1]
            table.append(
                [task.id, task.task, task.project, task.status, task.tag,
                 round_timedelta(duration), task.due_date])
    except UnboundLocalError:
        pass
    return table


def pop_up_msg():
    """Pop up finish msg"""
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Your Time is Over! Well done!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()


def make_table_projects(engine, tasks):
    table = [['id', 'Task', 'Status', 'Tag', 'hh:mm', 'Due in']]
    try:
        project_duration = timedelta()
        for i in list_query(engine, tasks):
            task = i[0]
            duration = i[1]
            project_duration += duration
            table.append(
                [task.id, task.task, task.status, task.tag,
                 round_timedelta(duration), task.due_date])
    except UnboundLocalError:
        pass
    return table, round_timedelta(project_duration)


