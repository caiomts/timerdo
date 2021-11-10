from datetime import datetime, timedelta, date
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
import numpy as np


class Project(SQLModel, table=True):
    """SQL table and table instances for projects"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tasks: List['ToDo'] = Relationship(back_populates='project')

    timers: Optional[List['Timer']] = Relationship(back_populates='project')

    duration: Optional[timedelta] = None


class DueDate(SQLModel, table=True):
    """Due dates table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    due_date: date

    tasks: List['ToDo'] = Relationship(back_populates='due_date')


class Reminder(SQLModel, table=True):
    """Reminder"""
    id: Optional[int] = Field(default=None, primary_key=True)
    reminder: date

    tasks: List['ToDo'] = Relationship(back_populates='reminder')


class ToDo(SQLModel, table=True):
    """SQL table and table instance for the 'to do' list"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_int: date = date.today()
    data_end: Optional[date] = None
    task: str
    status: str
    tag: Optional[str] = None
    remarks: Optional[str] = None

    project_id: Optional[int] = Field(foreign_key='project.id')
    project: Optional[Project] = Relationship(back_populates='tasks')

    due_date_id: Optional[int] = Field(foreign_key='duedate.id')
    due_date: Optional[DueDate] = Relationship(back_populates='tasks')

    reminder_id: Optional[int] = Field(foreign_key='reminder.id')
    reminder: Optional[Reminder] = Relationship(back_populates='tasks')

    timers: Optional[List['Timer']] = Relationship(back_populates='task')

    duration: Optional[timedelta] = None


class Timer(SQLModel, table=True):
    """SQL table and table instance for the timer schedule"""
    id: Optional[int] = Field(default=None, primary_key=True)
    id_todo: Optional[int] = Field(foreign_key='todo.id')
    start: datetime = datetime.now()
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None

    task: ToDo = Relationship(back_populates='timers')

    project: Optional[Project] = Relationship(back_populates='timers')


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
