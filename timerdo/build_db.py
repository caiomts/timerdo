from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import SQLModel, create_engine, Field, Relationship


class ToDo(SQLModel, table=True):
    """SQL table and table instance for the 'to do' list"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date_int: datetime = datetime.now()
    data_end: Optional[datetime] = None
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


sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()


if __name__ == '__main__':
    main()
