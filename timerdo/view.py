from dataclasses import dataclass

from timerdo.build_db import ToDo


@dataclass
class View:
    """Class for view"""
    due_task: ToDo = ''
    today_task: ToDo = ''
    week_task: ToDo = ''

    simple_task: ToDo = ''

    reminders: ToDo = ''

    def load_view(self ,engine):

