from datetime import datetime, timedelta, date
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class ToDo(SQLModel, table=True):
    """SQL table and table instance for the 'to do' list"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_int: date = date.today()
    data_end: Optional[date] = None
    project: Optional[str] = None
    task: str
    due_date: Optional[datetime] = None
    reminder: Optional[datetime] = None
    duration: Optional[timedelta] = None
    status: str
    tag: Optional[str] = None
    remarks: Optional[str] = None

    timer: Optional['Timer'] = Relationship(back_populates='todo')


class Timer(SQLModel, table=True):
    """SQL table and table instance for the timer schedule"""
    id: Optional[int] = Field(default=None, primary_key=True)
    id_todo: Optional[int] = Field(foreign_key='todo.id')
    start: datetime = datetime.now()
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None

    todo: ToDo = Relationship(back_populates='timer')


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
