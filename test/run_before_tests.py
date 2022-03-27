import os

from run_after_tests import after

from timerdo.database import app_dir, sqlite_file_name


def before():
    """Make copy of production database."""
    if os.path.exists(os.path.join(app_dir, 'test.db')):
        after()

    os.rename(sqlite_file_name, os.path.join(app_dir, 'test.db'))


if __name__ == '__main__':
    before()
