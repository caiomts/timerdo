# Introduction

Timerdo is a CLI application to help you improve your productivity and 
keep track of your work. 

**Timerdo was thought to track tasks, so tasks are its building blocks. 
Keep that in mind.**

*Done is Done. You can't do anything else with a task once it's done.*

## Requirements

Timerdo is 100% python, so pip installation should work regardless of your OS.

Timerdo requires python 3.9 or higher. It relies on SQLite database to maintain 
your records. It is basically built with
[SQLModel](https://sqlmodel.tiangolo.com/),
[Typer](https://typer.tiangolo.com/) and
[Rich](https://rich.readthedocs.io/en/stable/index.html).

## Installation

You can install timerdo from PyPI with pip or your favorite package manager. 
Although I do recommend to use [pipx](https://pypa.github.io/pipx/) to install
and manage your CLI applications.

```console
$ pipx install timerdo
```
    
## Quick start

The only way to start with timerdo is *adding* a task and timerdo will 
take care of all the boilerplate for you. So, just call `add`.

```console
$ timerdo add "<your task goes here>"
[22:25:25] Added new entry with ID 1.
```

Now that you already have a task recorded you can start tracking your time for
that task.

The easiest way to `start` the timer is knowing the task id (it was showed in the 
output above).

```console
$ timerdo start <task id goes here>
[08:14:51] <your task> has just started. Timer id: <task id>
```

After you have done a lot of work, you can `stop` your timer. 
If you have done the task and you do not need working on it anymore, you should answer `y`
and Timerdo will keep it out of your way, otherwise type `n` to work in the same task 
in the future.

```console
$ timerdo stop
Is the task done?
 [y/n]:
```

Timerdo has a lot of ways to visualize your tasks, but the simplest one is just call `list` command and it prints some tables like these ones below. 

```console
$ timerdo list
╭─────────────────────────── THIS WEEK SHORT SUMMARY ───────────────────────────╮
│ Finished 8 tasks this week                          Worked 15 hours this week │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────── OVERDUE ───────────────────────────────────╮
│ Tasks: 1                                                                      │
│                                                                               │
│      ID   Task                       Project   Status   Time on     Delayed   │
│  ───────────────────────────────────────────────────────────────────────────  │
│       2   Democratic have media      True.     to do    5 hours   9117 days   │
│           over political but.                                                 │
│                                                                               │
│   Total                                                 5 hours               │
│                                                                               │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────── TASKS WITHOUT DUE DATE ────────────────────────────╮
│ Tasks: 1                                                                      │
│                                                                               │
│      ID   Task                  Project         Status   Time on   Duration   │
│  ───────────────────────────────────────────────────────────────────────────  │
│      11   Memory adult          Second happy.   to do    8 hours     0 days   │
│           Republican old                                                      │
│           think executive                                                     │
│           address benefit.                                                    │
│                                                                               │
│   Total                                                  8 hours              │
│                                                                               │
╰───────────────────────────────────────────────────────────────────────────────╯
```

Finally, Timerdo also has a *help* function where you can find all available commands
with short descriptions. You just have call `--help`.

```console
$ timerdo --help
Usage: timerdo [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  add     Add new task to database.
  edit    Edit records.
  list    List tasks.
  report  Print customized reports.
  start   Start Timer for a given open task.
  stop    Stop a running task.
```
To see more about how to manage **Timerdo** follow along this documentation.




