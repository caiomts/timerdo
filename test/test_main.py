from datetime import datetime

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
    assert '╭─────' in result.stdout


def test_version():
    result = runner.invoke(app, ['--version'])
    assert f'Timerdo version: {__version__}' in result.stdout


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
    result = runner.invoke(app, ['stop', '-d'])
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
    result = runner.invoke(app, ['query', 'SELECT * FROM todo_list'])
    assert '{' in result.stdout


def test_delete_timer():
    result = runner.invoke(app, ['delete', 'timer', '1'])
    assert result.exit_code == 0


def test_delete_task():
    result = runner.invoke(app, ['delete', 'task', '1'])
    assert result.exit_code == 0


def test_report():
    result = runner.invoke(
        app, ['report', '--order-by', 'test', '--tag', 'test']
    )
    assert f'from 1789-07-14 until {datetime.now().date()}' in result.stdout


def test_report_date():
    result = runner.invoke(
        app, ['report', '--init', '1988-10-10', '--end', '2022-10-10']
    )
    assert 'from 1988-10-10 until 2022-10-10' in result.stdout


def test_report_date_init():
    result = runner.invoke(app, ['report', '--init', '1988-10-10'])
    assert f'from 1988-10-10 until {datetime.now().date()}' in result.stdout


def test_report_date_end():
    result = runner.invoke(app, ['report', '--end', '1988-10-10'])
    assert 'from 1789-07-14 until 1988-10-10' in result.stdout


def test_report_date_error():
    result = runner.invoke(
        app, ['report', '--end', '1400-10-10', '--init', '1988-10-10']
    )
    assert result.exit_code == 1


def test_delete_test(delete_test):
    pass
