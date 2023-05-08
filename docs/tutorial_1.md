
# User Guide (CUD of CRUD Tasks) - Timer, Delete and Update

CRUD is an acronym. They are the four basic operations for persistent storage[^1]

!!! info "*TL;DR*"

    In this section we'll discuss all the features in depth so if you are already using
    Timerdo and in a hurry, just go straight to any section or to the [reference](cli_reference.md).

!!! Danger "Technicalities"
    If you are not into Python or Timerdo internals you should skip all these notes.


## Tasks

We already know how to create a [simple task](start.md#adding-your-first-task).
But how to add *Deadline* or tag your task?

All good CLI applications have a `--help` flag to help you. 
They're usually short and don't replace a User Manual or Guide, 
but they're a good start and perfect for quickly remembering things.

```shell linenums="1"
$ timerdo task --help
                                                                                             
 Usage: timerdo task [OPTIONS] TASK                                                          
                                                                                             
 Add a task to the To-Do list.                                                               
                                                                                             
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────╮
│ *    task      TEXT  Task to be add to To-Do list. [default: None] [required]             │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --tag       -t      TEXT                Task tag. [default: None]                         │
│ --deadline  -d      [%Y-%m-%d]          Task Deadline. [default: None]                    │
│ --status    -s      [To Do|Doing|Done]  Task Status. [default: To Do]                     │
│ --help                                  Show this message and exit.                       │
╰───────────────────────────────────────────────────────────────────────────────────────────╯

```

Let's start with line 3. In lower case you see the command we passed to the terminal `timerdo task`. 
In upper case `[OPTIONS]` and `TASK`. What does it means? 

Both are listed in `Arguments` and `Options` tables just below. 
In this case, we have a positional argument `TASK` which is required (as you can see on line 8). 
`TASK` has a defined type (`TEXT`) and is literally a text that describes the task you'd like to add to the list.

The table `Options` has 4 options, none of them are required and that's how we could add a task in the previous section
just by describing it. The last option is the `--help`. This option will overide everything and just show the same message above.


??? tip "Call for `--help`"
    Call for `--help` at any time. All commands have their own help page as well.
    ```shell
    $ timerdo --help

     Usage: timerdo [OPTIONS] COMMAND [ARGS]...                                                  
                                                                                             
     Timerdo is a minimalist to-do list with built-in timer to keep your tasks on track.         

    ╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
    │ --version             -v        Print version.                                            │
    │ --install-completion            Install completion for the current shell.                 │
    │ --show-completion               Show completion for the current shell, to copy it or      │
    │                                 customize the installation.                               │
    │ --help                          Show this message and exit.                               │
    ╰───────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ────────────────────────────────────────────────────────────────────────────────╮
    │ delete      Delete item, given table and item id.                                         │
    │ edit        Edit task or timer entries.                                                   │
    │ query       Query the data with sql script and return a json.                             │
    │ report      Print reports.                                                                │
    │ start       Start timer.                                                                  │
    │ stop        Stop running timer.                                                           │
    │ task        Add a task to the To-Do list.                                                 │
    ╰───────────────────────────────────────────────────────────────────────────────────────────╯

    ```

### tag

Let's take a look at line 11. `--tag` is the *Task tag*, defaults to `None` and has a defined type (`TEXT`). Let's see how it works
in practice.

```shell
$ timerdo task "my very new task with options" --tag "user guide tag"
$ timerdo report

                                                                                             
                                                             from 1789-07-14 until 2023-05-04
                                                                                             

                    🏷️      ---   0 days 00:04:08                    
                                                                    
╭────┬────────────┬───────────────────────┬──────────┬────────┬─────────────────╮
│ ID │       Date │ Task                  │ Deadline │ Status │      Time       │
├────┼────────────┼───────────────────────┼──────────┼────────┼─────────────────┤
│  1 │ 2023-05-04 │ <your task goes here> │          │ Doing  │ 0 days 00:04:08 │
╰────┴────────────┴───────────────────────┴──────────┴────────┴─────────────────╯

                       🏷️   User Guide Tag   ---   0 days 00:00:00                        
                                                                                         
╭────┬────────────┬───────────────────────────────┬──────────┬────────┬─────────────────╮
│ ID │       Date │ Task                          │ Deadline │ Status │      Time       │
├────┼────────────┼───────────────────────────────┼──────────┼────────┼─────────────────┤
│  2 │ 2023-05-04 │ My Very New Task With Options │          │ To Do  │ 0 days 00:00:00 │
╰────┴────────────┴───────────────────────────────┴──────────┴────────┴─────────────────╯

```
Now when you call for `report`, Timerdo wraps the tags. Instead of using `--tag` you can also use the
shortcut `-t` - you know too many letters to type :sweat_smile:.

### deadline

At line 12, `--deadline` has a different type (`[%Y-%m-%d]`). In this case, It's a date type
and the structure is year-month-day as in 1789-07-14.

Let's try it out:

```shell
$ timerdo task "my second task with options" --tag "user guide tag" -d 2023-05-10
$ timerdo report
    --/-- More things above --/--

╭────┬────────────┬─────────────────────────────┬────────────┬────────┬─────────────────╮
│ ID │       Date │ Task                        │   Deadline │ Status │      Time       │
├────┼────────────┼─────────────────────────────┼────────────┼────────┼─────────────────┤
│  3 │ 2023-05-04 │ My Second Task With Options │ 2023-05-10 │ To Do  │ 0 days 00:00:00 │

    --/-- More things below --/--
```
Here we used the `--deadline` shortcut (`-d`).

??? danger "Technicalities" 
    `--deadline` is in the CLI API a `#!python datetime` and not a `#!python date` as [Typer](https://typer.tiangolo.com/) -
    the library for building CLI apps I used - doesn't support `#!python date`. 
    However the Timerdo core treats it as a `#!python date` and the data model maps it as `date` as well.

### status

`--status` is the last option we can use with `task` command. 
It has a pre-defined type (`[To Do|Doing|Done]`) and defaults to `To Do`.

Let's try a new task:

```shell
$ timerdo timerdo task "my second task with options" --Status "to do"
Usage: timerdo task [OPTIONS] TASK
Try 'timerdo task --help' for help.
╭─ Error ───────────────────────────────────────────────────────────────────────────────────╮
│ Invalid value for '--status' / '-s': 'to do' is not one of 'To Do', 'Doing', 'Done'.      │
╰───────────────────────────────────────────────────────────────────────────────────────────╯

```
It raised an error. Why?

You must precisely "To Do" instead of "to do". `--status` is case sensitive.

??? danger "Technicalities"
    Here who raised an error was Typer and not Timerdo. Typer is fully typed and `status` must receive a Status
    object.

    ```py title="models.py" linenums="14"
    class Status(StrEnum):
        """Status class."""

        to_do = 'To Do'
        doing = 'Doing'
        done = 'Done'
    ```

In the next topics we'll come back to the `status` option to set it properly.

## Timer

You already know everything about Timer. It has only 2 commands [`start`](start.md#starting-the-timer) 
and [`stop`](start.md#stopping-the-timer).
To start the timer you need to let it know the task you're going to work on and to stop whether or not your
task is done.

### start

Let's see the `--help` one more time.

```shell
$ timerdo start --help
                                                                                             
 Usage: timerdo start [OPTIONS] TASK_ID                                                      
                                                                                             
 Start timer.                                                                                
                                                                                             
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────╮
│ *    task_id      INTEGER  task id for timing. [default: None] [required]                 │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

`task_id` is a integer and also a required argument. It is the `id`
of one task in your to do list.

### stop

To stop the timer you don't need any argument, but you can flag beforehand if
your task was done or not using the flag `--done` or the shortcut `-d`.

Let's see how to flag it.

```shell
$ timerdo stop --done
```

Flag is the same as calling an option with no variable. as simple as that.

??? tip
    Flag are usually used for boolean variables. When you flag something you are
    saying that it's `TRUE`.


## delete

Until now you didn't make a mistake :clap:. But you know, humans make mistakes.
Let's say your are human and made a miskate. The very first solution is to throw it away.

To delete a entry you have 2 arguments `table` and `id`.

`table` are: `[task|timer]`. It works in the same way of `status`. `id` you already know.
Each table has its own ids.

```shell
$ timerdo delete timer 1
$ timerdo report
    --/-- More things above --/--                                            
╭────┬────────────┬───────────────────────┬──────────┬────────┬─────────────────╮
│ ID │       Date │ Task                  │ Deadline │ Status │      Time       │
├────┼────────────┼───────────────────────┼──────────┼────────┼─────────────────┤
│  1 │ 2023-05-04 │ <your task goes here> │          │ Doing  │ 0 days 00:00:00 │
╰────┴────────────┴───────────────────────┴──────────┴────────┴─────────────────╯
    --/-- More things below --/--
```
??? warning
    If you delete a task, all timers linked to that task will be deleted as well.

Sometimes everything is almost correctly and you don't want to delete everything.
The next topic will show you how to update your data.

??? warning "Under construction :factory_worker:"
    Up to this point you can query using sql script (I'll show later on) to create personal
    reports. it returns a json. 
    
    This is, so far, the only way to view the Timer table.

    You can copy and past the script when the time comes: "SELECT * FROM timer_list"

    These are the planned steps:

    **Reports**

    - [ ] Create one simple timer reports with period filter.
    - [ ] Create one simple task report with period filter.
    - [ ] Create a CLI entry point to call both functions from one subcommand (like edit or delete).
    
    **Delete**
    
    - [ ] Update delete function to delete batches by *tag*.
    - [ ] Update delete function to delete by *creation* period.


## Update

In Timerdo you can `edit` both tables, but one row at a time.
You have basically two commands `task` and `timer` and each one you have a
required argument `id`, or the row you want to edit, and as options as the number
of columns in the table. Now you already know how to can call `--help`,
you can call each in each commant to see all possibilities.

Let's see the `--help` for Timer as we didn't see the structure before.

```shell
$ timerdo edit timer --help
                                                                                             
 Usage: timerdo edit timer [OPTIONS] ID                                                      
                                                                                             
 Edit a timer item.                                                                          
                                                                                             
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────╮
│ *    id      INTEGER  Item id. [default: None] [required]                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --create_at    -c      [%Y-%m-%d %H:%M:%S]  timer start. [default: None]                  │
│ --finished_at  -f      [%Y-%m-%d %H:%M:%S]  timer stop. [default: None]                   │
│ --help                                      Show this message and exit.                   │
╰───────────────────────────────────────────────────────────────────────────────────────────╯

```

You can edit two variables `--created_at` and `--finished_at`, or the moment you start and stop
the Timer. the structure is similar to date in [deadline](tutorial_1.md#deadline), but now
you need to set also hour:minutes:seconds (`%H:%M:%S`) and the format is "1789-07-14 22:20:10".

Now you know how to *Create*, *Update* and *Delete* in depth, let's deep dive into how to `report` and
`query` your data in the next section.


[^1]: Persistence is the characteristic of data that outlive the process that created it. 
In Timerdo, we are talking about the basic operations to interact with our database.