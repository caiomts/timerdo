# User Guide  (R of CRUD) - Retrieve Your Data.

Currently Timerdo has to ways to retrieve your data through CLI entry points. 
The first way is the standard way of doing it. The second way has two goals: 
to give you total freedom and control over your own data and 
to work as compatible output to pipe as input into another CLI application.

??? Danger "Technicalities"
    When using CLI applications, it is quite common to use different applications in sequence. Output from one application is used as input to another application. Connecting applications is like building a "pipeline" so you need to use "pipes" (> or >>) to direct an output as an input to the next application. I'll show an example when explaining the `query` Timerdo command.


## Report

`report` is the standard way to retrieve your data. It has one print pattern
that you already know and 5 options to fine-tune your report. Here we'll stick to the
code blocks as they are easier to show off things and don't clutter the documentation,
but remember that the real one is [fancier](https://caiomts.github.io/timerdo/start/#reporting-your-tasks) than this one.

`report` group your tasks per `tag`. In the example below we have three different
tags, thus 3 different tables. 


```shell linenums="1"
$ timerdo report
                                                             from 1789-07-14 until 2023-05-08
                                                                                             

                            🏷️   Customer   ---   0 days 01:04:02                             
                                                                                             
╭────┬────────────┬─────────────────────────────────┬────────────┬────────┬─────────────────╮
│ ID │       Date │ Task                            │   Deadline │ Status │      Time       │
├────┼────────────┼─────────────────────────────────┼────────────┼────────┼─────────────────┤
│  3 │ 2023-05-08 │ White Interesting Bag Machine   │ 1998-02-08 │ Doing  │ 0 days 00:10:42 │
│    │            │ Store.                          │            │        │                 │
│  2 │ 2023-05-08 │ Certain Follow Plant.           │ 1996-07-07 │ Doing  │ 0 days 00:02:00 │
│  1 │ 2023-05-08 │ Leave Option President Bag      │ 2022-02-16 │ Doing  │ 0 days 00:51:20 │
│    │            │ Identify Last History Strategy. │            │        │                 │
╰────┴────────────┴─────────────────────────────────┴────────────┴────────┴─────────────────╯

                             🏷️   Speech   ---   0 days 01:31:35                             
                                                                                            
╭────┬────────────┬────────────────────────────────┬────────────┬────────┬─────────────────╮
│ ID │       Date │ Task                           │   Deadline │ Status │      Time       │
├────┼────────────┼────────────────────────────────┼────────────┼────────┼─────────────────┤
│  8 │ 2023-05-08 │ Campaign Learn Picture Send.   │ 1994-11-12 │ Doing  │ 0 days 01:11:02 │
│  7 │ 2023-05-08 │ Something Life Pm Month.       │ 2015-01-20 │ Doing  │ 0 days 00:20:33 │
│  6 │ 2023-05-08 │ Own Together Speech Major Guy. │ 2002-03-24 │ Doing  │ 0 days 00:00:00 │
╰────┴────────────┴────────────────────────────────┴────────────┴────────┴─────────────────╯

                               🏷️   Tv   ---   0 days 00:00:00                                
                                                                                             
╭────┬────────────┬─────────────────────────────────┬────────────┬────────┬─────────────────╮
│ ID │       Date │ Task                            │   Deadline │ Status │      Time       │
├────┼────────────┼─────────────────────────────────┼────────────┼────────┼─────────────────┤
│  5 │ 2023-05-08 │ Throw Small Source.             │ 2013-08-02 │ To Do  │ 0 days 00:00:00 │
│  4 │ 2023-05-08 │ Place Identify Best Project     │ 1994-02-02 │ To Do  │ 0 days 00:00:00 │
│    │            │ Drop Fight Democrat.            │            │        │                 │
╰────┴────────────┴─────────────────────────────────┴────────────┴────────┴─────────────────╯

```

### Report Time frame

In the second line of the report we have the time frame that was took into consideration to
generate the report. Every `timer` within the time frame was added to generate the report.

You can set the lower boundary with `--init` (shortcut: `-i`) and the upper boundary with `--end` (shortcut: `-e`).

??? warning
    1. The range is mathematically defined as **[initial; final)**. Which means that all timers equal to or greater than the initial one are considered, but only timers less than the final one are considered.

    2. `Timers` are defined by date plus time, however you can define the frame using only date, consequently your time is predefined to `00:00` and you need to always define the next day to aggregate all Previous day's `timers`.

    3. If you don't set the upper boundary it will print today as default, but in this case it'll take into account all `timers` in the table.


### Report per tag

The header of each table (lines 5, 17 and 27) is represented by the `tag` in which the tasks were grouped
and the total amount of time spent in the `tag`, in other words, the sum of all times spent in each task 
tagged the same way.

You can filter your report by tag with the option `--tag` (shortcut: `-t`).

??? tip
    You can pass how many `tags` you want using the option `--tag` for each `tag`. 

    ```shell
    $ timerdo report --tag "<your first tag>" --tag "<your second tag>"
    ``` 

### Report done tasks

When you call the report with no options, Timerdo will only report uncompleted tasks,
but you may need to have also an overview of all tasks. You can flag the `--done` (shortcut: `-d`)
option to print also `Done` tasks.

### Order tasks

You can order or tasks by `date`, `deadline`, `status` and `task` using the option `--order-by` (`-o`) combined with the flag `--asc` (`-a`) to ascending order.

## Query

Using the `query` command, Timerdo gives you superpowers to retrieve your data. This command has only one argument (`script`) which you can pass any sql script to Timerdo to query your data and create your report. This command generates a JSON that you can also pipe to another application.

The following command queries your Timer table and saves it as JSON to a file in your working directory.

```shell
$ timerdo query "SELECT * FROM timer_list" > file_name.json
```

??? Danger "Technicalities"
    Timerdo has a SQLite database with two tables: `timer_list` and `todo_list`.
    You can see the models below.

    ```py title="models.py" linenums="31"
    class ToDoItem(Base):
    """Todo Item class."""

    __tablename__ = 'todo_list'

    id = mapped_column(Integer, primary_key=True, init=False)
    task: Mapped[str] = mapped_column(String)
    tag: Mapped[str | None] = mapped_column(String, default=None)
    deadline: Mapped[date | None] = mapped_column(Date, default=None)
    status: Mapped[Status] = mapped_column(String, default=Status.to_do)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.utcnow(), default=None
    )

    timers: Mapped[list['Timer']] = relationship(
        back_populates='todo_item',
        cascade='all, delete-orphan',
        default_factory=list,
        init=False,
    )


    class Timer(Base):
        """Timer item class."""

        __tablename__ = 'timer_list'

        id = mapped_column(Integer, primary_key=True, init=False)
        task_id: Mapped[int] = mapped_column(ForeignKey('todo_list.id'))
        created_at: Mapped[datetime] = mapped_column(
            insert_default=datetime.utcnow(), default=None
        )
        finished_at: Mapped[datetime | None] = mapped_column(
            DateTime, default=None
        )

        todo_item: Mapped['ToDoItem'] = relationship(
            back_populates='timers', init=False
        ) 
    ```


## Config

??? warning "Under construction :factory_worker:"
    Up to this point, you cannot save your configuration for reporting or querying your data. Timerdo already has this in mind, but it hasn't been implemented yet.

    Planned steps:

    - [ ] Create a TOML config layout.
    - [ ] upgrade `report` and `query` to read config file.

    If you are interested in the next "Technicalities" you can see how Timerdo has already a function
    to read the config file and how it finds and saves this file.


??? Danger "Technicalities"
    When installing Timerdo and calling it for the first time, Timerdo will try to connect to your database in a default directory (depends on your operating system). If it fails, Timerdo will create the folder and database for you. In order to have full control of your data and be able to move your database or delete the entire Timerdo, you need to know how to find your database. Below I reproduce part of the script that Timerdo uses to manipulate its database.

    ```py title="config.py" linenums="6"
    def get_user_dir(dir_data: bool = True) -> Path:
    """Get user directories."""
    home = Path.home()
    env_test = os.environ.get('TIMERDOTEST', '')
    match platform.system(), env_test:
        case 'Windows', '':
            if os.getenv('APPDATA'):
                return Path(os.getenv('APPDATA'))
            else:
                return Path(os.getenv('LOCALAPPDATA'))
        case 'Darwin', '':
            return Path(home, 'Library')
        case _, '':
            if dir_data is True:
                return Path(home, '.local/share')
            else:
                return Path(home, '.config')
        case _, _:
            return Path(os.environ['TIMERDOTEST']) / 'TimerdoTest'


    data_dir = get_user_dir() / 'Timerdo'
    config_dir = get_user_dir(dir_data=False)

    data_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    ```
