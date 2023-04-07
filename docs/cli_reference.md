# `timerdo`

Timerdo is a minimalist to-do list with built-in timer
to keep your tasks on track.

**Usage**:

```console
$ timerdo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `delete`: Delete item, given table and item id.
* `edit`: Edit task or timer entries.
* `query`: Query the data.
* `start`: Start timer.
* `stop`: Stop running timer.
* `task`: Add a task to the To-Do list.

## `timerdo delete`

Delete item, given table and item id.

**Usage**:

```console
$ timerdo delete [OPTIONS] TABLE:{task|timer} ID
```

**Arguments**:

* `TABLE:{task|timer}`: Table containing the item.  [required]
* `ID`: Item id.  [required]

**Options**:

* `--help`: Show this message and exit.

## `timerdo edit`

Edit task or timer entries.

**Usage**:

```console
$ timerdo edit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `task`: Edit a task item.
* `timer`: Edit a timer item.

### `timerdo edit task`

Edit a task item.

**Usage**:

```console
$ timerdo edit task [OPTIONS] ID
```

**Arguments**:

* `ID`: Item id.  [required]

**Options**:

* `-t, --task TEXT`: Task
* `--tag TEXT`: Task tag.
* `-d, --deadline [%Y-%m-%d]`: Task Deadline.
* `-s, --status [To Do|Doing|Done]`: Task Status.
* `--help`: Show this message and exit.

### `timerdo edit timer`

Edit a timer item.

**Usage**:

```console
$ timerdo edit timer [OPTIONS] ID
```

**Arguments**:

* `ID`: Item id.  [required]

**Options**:

* `-c, --create_at [%Y-%m-%d %H:%M:%S]`: timer start.
* `-f, --finished_at [%Y-%m-%d %H:%M:%S]`: timer stop.
* `--help`: Show this message and exit.

## `timerdo query`

Query the data.

**Usage**:

```console
$ timerdo query [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `sql`: Query the data with sql.

### `timerdo query sql`

Query the data with sql.

**Usage**:

```console
$ timerdo query sql [OPTIONS] [SQL]
```

**Arguments**:

* `[SQL]`: Item id.  [default: 
        SELECT td.id, task, tag, deadline, status, sum(
            strftime('%M', finished_at) - strftime('%M', tl.created_at)
            ) as time
        FROM todo_list as td
        LEFT OUTER JOIN timer_list as tl
        ON tl.task_id = td.id
        GROUP BY td.id, task, tag, deadline, status
        ORDER BY deadline ASC
        ]

**Options**:

* `--help`: Show this message and exit.

## `timerdo start`

Start timer.

**Usage**:

```console
$ timerdo start [OPTIONS] TASK_ID
```

**Arguments**:

* `TASK_ID`: task id for timing.  [required]

**Options**:

* `--help`: Show this message and exit.

## `timerdo stop`

Stop running timer.

**Usage**:

```console
$ timerdo stop [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `timerdo task`

Add a task to the To-Do list.

**Usage**:

```console
$ timerdo task [OPTIONS] TASK
```

**Arguments**:

* `TASK`: Task to be add to To-Do list.  [required]

**Options**:

* `--tag TEXT`: Task tag.
* `-d, --deadline [%Y-%m-%d]`: Task Deadline.
* `-s, --status [To Do|Doing|Done]`: Task Status.  [default: To Do]
* `--help`: Show this message and exit.
