from datetime import date, timedelta
from enum import Enum

from rich import box, print
from rich.panel import Panel
from rich.table import Table
from sqlmodel import Session, select

from .tables import Timer


class Status(str, Enum):
    """Status."""

    to_do = 'to do'
    doing = 'doing'
    done = 'done'


def calculate_timer_per_task(task_list: list, engine):
    with Session(engine) as session:
        time_tasks = {}
        for task in task_list:
            id_todo = task.id
            timer_list = session.exec(
                select(Timer).where(Timer.id_todo == id_todo)
            ).all()
            time_tasks[id_todo] = sum(
                [
                    (timer.end - timer.start).total_seconds() / 3600
                    for timer in timer_list
                    if timer.end is not None
                ]
            )
    return time_tasks


def calculate_work_per_week(engine):
    first_weekday = date.today() - timedelta(
        days=(date.today().isocalendar()[2])
    )
    with Session(engine) as session:
        timer_list = session.exec(
            select(Timer).where(Timer.start >= first_weekday)
        ).all()
        time_tasks = sum(
            [
                (timer.end - timer.start).total_seconds() / 3600
                for timer in timer_list
                if timer.end is not None
            ]
        )
    return time_tasks


class View:
    def __init__(self, row_list, engine):
        """Views."""
        self.row_list = row_list
        self.total_task = len(row_list)
        self.engine = engine

        self.timers = calculate_timer_per_task(self.row_list, self.engine)

        self.col_id = {
            'header': 'ID',
            'justify': 'right',
            'style': 'cyan',
            'no_wrap': True,
        }
        self.col_init = {
            'header': 'Started in',
            'justify': 'right',
            'no_wrap': True,
        }
        self.col_end = {
            'header': 'Ended in',
            'justify': 'right',
            'no_wrap': True,
        }
        self.col_task = {
            'header': 'Task',
        }
        self.col_project = {'header': 'Project', 'no_wrap': True}
        self.col_tag = {'header': 'Tag', 'justify': 'center', 'no_wrap': True}
        self.col_status = {
            'header': 'Status',
            'justify': 'center',
            'no_wrap': True,
        }
        self.col_due_date = {
            'header': 'Due Date',
            'style': 'yellow',
            'justify': 'right',
            'no_wrap': True,
        }
        self.col_reminder = {'header': 'Reminder', 'no_wrap': True}
        self.col_time_on = {
            'header': 'Time on',
            'justify': 'right',
            'no_wrap': True,
        }
        self.col_delayed = {
            'header': 'Delayed',
            'justify': 'right',
            'style': 'yellow',
            'no_wrap': True,
        }
        self.col_days_from_init = {
            'header': 'Duration',
            'justify': 'right',
            'style': 'yellow',
            'no_wrap': True,
        }

    def plot_list(self, type_, ref_date):
        """Plot list panel."""
        table = Table(
            title=f'Tasks: {self.total_task}',
            title_justify='full',
            box=box.SIMPLE,
            expand=True,
        )
        table.add_column(**self.col_id)
        table.add_column(**self.col_task)
        table.add_column(**self.col_project)
        table.add_column(**self.col_status)
        table.add_column(**self.col_time_on)

        title = f'REMINDERS IN {date.today()}'
        border_style = 'blue'
        if type_ == 'overdue':
            table.add_column(**self.col_delayed)
            title = 'OVERDUE'
            border_style = 'red'
        if type_ == 'due_in':
            table.add_column(**self.col_due_date)
            title = f'DUE UNTIL {ref_date}'
            border_style = 'yellow'
        if type_ == 'no_due':
            table.add_column(**self.col_days_from_init)
            title = 'TASKS WITHOUT DUE DATE'
            border_style = 'green'

        total_worked = 0
        for task in self.row_list:
            plot_row = None

            if type_ == 'overdue':
                delayed = ref_date - task.due_date
                plot_row = f'{delayed.days} days'
            if type_ == 'due_in':
                plot_row = f'{task.due_date}'
            if type_ == 'no_due':
                total_days = date.today() - task.date_init
                plot_row = f'{total_days.days} days'

            total_worked += self.timers[task.id]
            table.add_row(
                str(task.id),
                task.task,
                task.project,
                task.status,
                f'{int(round(self.timers[task.id]))} hours',
                plot_row,
            )
        table.add_row()
        table.add_row(
            '[bold]Total',
            None,
            None,
            None,
            f'{int(round(total_worked))} hours',
            None,
        )

        print(Panel(table, title=title, border_style=border_style))

    def week_summary(self):
        """Plot week summary."""
        work_per_week = calculate_work_per_week(self.engine)

        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify='right')
        grid.add_row(
            f'Finished [green]{len(self.row_list)} [white]tasks this week',
            f'Worked [green]{int(work_per_week)} [white]hours this week',
        )
        print(
            Panel(grid, title='THIS WEEK SHORT SUMMARY', border_style='cyan')
        )
