from datetime import timedelta
import typer
from enum import Enum
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

        for task in query_list:
            duration = timedelta()
            for dur in task.timers:
                duration += dur.duration

    return query_list, duration


def make_table_view(engine, tasks):
    table = [['id', 'Task', 'Project', 'Status', 'Tag', 'hh:mm', 'Due in']]
    try:
        tasks, duration_ = list_query(engine, tasks)
        for task in tasks:
            table.append(
                [task.id, task.task, task.project, task.status, task.tag,
                 round_timedelta(duration_), task.due_date])
    except UnboundLocalError:
        pass

    return table



