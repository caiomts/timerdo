from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import data_dir
from .models import Base


class Connection:
    """Class with CRUD sections to comunicate with the database."""

    def __init__(self, engine):
        self.engine = engine
        self._session = sessionmaker(self.engine)

    def add(self, item):
        """Add item to the database."""
        with self._session.begin() as session:
            session.add(item)

    def delete(self, item):
        """Delete item from the database."""
        with self._session.begin() as session:
            session.delete(item)

    def get_id(self, model, id):
        """Get item from the database."""
        with self._session() as session:
            item = session.get(model, id)
        return item

    def execute(self, query):
        """Execute query in the database."""
        return self._session().execute(query)


database_path = data_dir / 'db_timerdo.db'

engine = create_engine(f'sqlite:///{database_path}', echo=False)

Base.metadata.create_all(engine)
