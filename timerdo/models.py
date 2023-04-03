from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Status(StrEnum):
    """Status class."""

    to_do = 'To Do'
    doing = 'Doing'
    done = 'Done'


class Base(
    MappedAsDataclass,
    DeclarativeBase,
):
    """Base class for models."""

    pass


class ToDoItem(Base):
    """Todo Item class."""

    __tablename__ = 'todo_list'

    id = mapped_column(Integer, primary_key=True, init=False)
    task: Mapped[str] = mapped_column(String)
    tag: Mapped[str | None] = mapped_column(String, default=None)
    deadline: Mapped[date | None] = mapped_column(Date, default=None)
    status: Mapped[Status] = mapped_column(String, default=Status.to_do)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.utcnow(), default=None
    )

    timers: Mapped[list['Timer']] = relationship(
        back_populates='todo_item',
        cascade='all, delete-orphan',
        default_factory=list,
        init=False,
    )


class Timer(Base):
    """Timer item class."""

    __tablename__ = 'timer_list'

    id = mapped_column(Integer, primary_key=True, init=False)
    task_id: Mapped[int] = mapped_column(ForeignKey('todo_list.id'))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.utcnow(), default=None
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None
    )

    todo_item: Mapped['ToDoItem'] = relationship(
        back_populates='timers', init=False
    )
