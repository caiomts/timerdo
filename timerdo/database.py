from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base

engine = create_engine('sqlite:///test.db', echo=True)

Base.metadata.create_all(engine)


def get_session():
    """Returns sql session."""
    return Session(engine)
