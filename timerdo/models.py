from datetime import datetime, date
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Date, func, Integer
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, relationship
)


class Status(StrEnum):
    to_do = 'To Do'
    doing = 'Doing'
    done = 'Done'


class Base(
    MappedAsDataclass,
    DeclarativeBase,
):
    pass


class ToDo(Base):
    __tablename__ = 'todo'

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
        init=False
    )


class Timer(Base):
    __tablename__ = 'timer'

    id = mapped_column(Integer, primary_key=True, init=False)
    task_id: Mapped[int] = mapped_column(ForeignKey('todo.id'))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.utcnow(), default=None
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None
    )

    todo_item: Mapped['ToDo'] = relationship(
        back_populates='timers', init=False
    )

