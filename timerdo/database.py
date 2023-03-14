from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .models import Base

engine = create_engine('sqlite:///test.db', echo=True)

Base.metadata.create_all(engine)

connection = sessionmaker(engine, expire_on_commit=False)
