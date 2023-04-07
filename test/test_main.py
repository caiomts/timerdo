from faker import Faker
from typer.testing import CliRunner

from timerdo.__init__ import __version__
from timerdo.main import app

fake = Faker()

runner = CliRunner()


def test_callback():
    result = runner.invoke(
        app,
    )
    assert f'timerdo Version: {__version__}' in result.stdout


def test_task():
    result = runner.invoke(
        app,
        [
            'task',
            f'{fake.sentence()}',
            '--tag',
            f'{fake.word()}',
            '--deadline',
            f'{fake.date_between()}',
        ],
    )
    assert result.exit_code == 0


def test_start():
    result = runner.invoke(app, ['start', '1'])
    assert result.exit_code == 0


def test_stop():
    result = runner.invoke(app, ['stop'])
    assert result.exit_code == 0


def test_edit_task():
    result = runner.invoke(
        app, ['edit', 'task', '1', '--task', f'{fake.sentence()}']
    )
    assert result.exit_code == 0


def test_edit_timer():
    result = runner.invoke(
        app, ['edit', 'timer', '1', '-c', f'{fake.date_time()}']
    )
    assert result.exit_code == 0


def test_query_sql():
    result = runner.invoke(app, ['query', 'sql'])
    assert '[' in result.stdout


def test_delete_timer():
    result = runner.invoke(app, ['delete', 'timer', '1'])
    assert result.exit_code == 0


def test_delete_task():
    result = runner.invoke(app, ['delete', 'task', '1'])
    assert result.exit_code == 0


def test_delete_test(delete_test):
    pass
