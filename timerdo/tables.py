from datetime import datetime, timedelta, date
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class ToDo(SQLModel, table=True):
    """SQL table and table instance for the 'to do' list"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_init: date = date.today()
    date_end: Optional[date] = None
    task: str
    status: str
    tag: Optional[str] = None
    remarks: Optional[str] = None
    due_date: Optional[date] = None
    reminder: Optional[date] = None
    project: Optional[str] = None

    timers: Optional[List['Timer']] = Relationship(back_populates='task')


class Timer(SQLModel, table=True):
    """SQL table and table instance for the timer schedule"""
    id: Optional[int] = Field(default=None, primary_key=True)
    id_todo: int = Field(foreign_key='todo.id')

    start: datetime = datetime.utcnow()
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None

    task: ToDo = Relationship(back_populates='timers')

