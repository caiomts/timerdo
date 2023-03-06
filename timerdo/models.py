from datetime import datetime, date
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Status(StrEnum):
    to_do = 'To Do'
    doing = 'Doing'
    done = 'Done'


class Base(DeclarativeBase):
    pass


class ToDo(Base):
    __tablename__ = 'todo_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String)
    tag: Mapped[str | None]
    deadline: Mapped[date | None]
    status: Mapped[Status] = mapped_column(String, default=Status.to_do)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    timers: Mapped[list['Timer']] = relationship(
        back_populates='todo', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'Task(id={self.id}, task={self.task}, tag={self.tag}, ' \
               f' status={self.status}, timestamp_utc={self.timestamp})'


class Timer(Base):
    __tablename__ = 'timer'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('todo_item.id'))
    start: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    stop: Mapped[datetime | None]

    todo: Mapped['ToDo'] = relationship(back_populates='timers')

    def __repr__(self) -> str:
        return f'Timer(id={self.id}, task_id={self.task_id}, ' \
               f'timestamp_utc={self.start})'
