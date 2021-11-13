import os
from pathlib import Path

import typer
from sqlmodel import SQLModel, create_engine

APP_NAME = 'timerdo'
app_dir = typer.get_app_dir(APP_NAME)
app_dir_path = Path(app_dir)
app_dir_path.mkdir(parents=True, exist_ok=True)

sqlite_file_name = os.path.join(app_dir, 'timerdo_db.db')

sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
