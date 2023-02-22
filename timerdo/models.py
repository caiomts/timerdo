from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)


class Base(DeclarativeBase):
    pass


class ToDo(Base):
    __tablename__ = 'todo_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String)
    tag: Mapped[str | None]
    status: Mapped[str] = mapped_column(String, default='To Do')

    timers: Mapped[list['Timer']] = relationship(
        back_populates='todo', cascade='all, delete-orphan'
    )
    

class Timer(Base):
    __tablename__ = 'timer'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('todo_item.id'))
    start: Mapped[datetime]
    end: Mapped[datetime | None]

    todo: Mapped['ToDo'] = relationship(back_populates='timers')