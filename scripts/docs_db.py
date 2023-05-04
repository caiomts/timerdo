from random import randint
from faker import Faker
from typer.testing import CliRunner
from timerdo.main import app

fake = Faker()

runner = CliRunner()


def generate_tasks():
    for tag in [fake.word(), fake.word(), fake.word()]:
        n = randint(2, 5)
        for i in range(n):
            if n % 2:
                status = 'Doing'
            else:
                status = 'To Do'
            runner.invoke(
                app,
                [
                    'task',
                    f'{fake.sentence()}',
                    '--tag',
                    tag,
                    '--deadline',
                    f'{fake.date_between()}',
                    '--status',
                    status
                ],
                    )
    

if __name__ == '__main__':
    generate_tasks()