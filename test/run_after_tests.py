import os

from timerdo.database import app_dir, sqlite_file_name


def after():
    """Delete test database."""
    try:
        os.remove(sqlite_file_name)
    except FileNotFoundError:
        pass
    os.rename(os.path.join(app_dir, 'test.db'), sqlite_file_name)


if __name__ == '__main__':
    after()
