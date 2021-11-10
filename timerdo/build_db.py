from datetime import datetime, timedelta, date
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Project(SQLModel, table=True):
    """SQL table and table instances for projects"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    name: str
    duration: Optional[timedelta] = None

    tasks: List['ToDo'] = Relationship(back_populates='project')

    timers: Optional[List['Timer']] = Relationship(back_populates='project')


class ToDo(SQLModel, table=True):
    """SQL table and table instance for the 'to do' list"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_init: date = date.today()
    data_end: Optional[date] = None
    task: str
    status: str
    tag: Optional[str] = None
    remarks: Optional[str] = None
    due_date: Optional[date] = None
    reminder: Optional[date] = None
    duration: Optional[timedelta] = None

    project_id: Optional[int] = Field(foreign_key='project.id')
    project: Optional[Project] = Relationship(back_populates='tasks')

    timers: Optional[List['Timer']] = Relationship(back_populates='task')


class Timer(SQLModel, table=True):
    """SQL table and table instance for the timer schedule"""
    id: Optional[int] = Field(default=None, primary_key=True)
    id_todo: int = Field(foreign_key='todo.id')
    id_project: Optional[int] = Field(foreign_key='project.id')

    start: datetime = datetime.now()
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None

    task: ToDo = Relationship(back_populates='timers')

    project: Optional[Project] = Relationship(back_populates='timers')


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
