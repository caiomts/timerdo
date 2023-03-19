from pathlib import Path
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


class Connection:
    """Class with CRUD sections to comunicate with the database."""
    def __init__(self, engine):
        self.engine = engine
        self._session = sessionmaker(self.engine)

    def add(self, item):
        with self._session.begin() as session:
            session.add(item)
        return True

    def delete(self, item):
        with self._session.begin() as session:
            session.delete(item)
        return True

    def get_id(self, model, id):
        with self._session() as session:
            item = session.get(model, id)
        return item

    def execute(self, query):
        return self._session().execute(query)


def get_db_dir():
    """Gets the folder path for saving the database."""
    home = Path.home()
    if sys.platform == 'darwin':
        folder = Path(home, 'Library')
    elif os.name == 'nt':
        appdata = os.environ.get('APPDATA', None)
        if appdata:
            folder = Path(appdata)
        else:
            folder = Path(home, 'AppData', 'Roaming')
    else:
        folder = Path(home, '.config')

    return folder / 'timerdo'


Path.mkdir(get_db_dir(), parents=True, exist_ok=True)

database_path = get_db_dir() / 'db_timerdo.db'

engine = create_engine(f'sqlite:///{database_path}', echo=True)

Base.metadata.create_all(engine)
