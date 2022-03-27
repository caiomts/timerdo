# Add

`add`, as the name suggests, adds new tasks to the database. As simple as that.

```console
$ timerdo add --help
Usage: timerdo add [OPTIONS] TASK

  Add new task to database.

Arguments:
  TASK  [required]

Options:
  -p, --project TEXT
  -d, --due-date [%Y-%m-%d]
  -r, --reminder [%Y-%m-%d]
  -s, --status [to do|doing|done]
                                  [default: Status.to_do]
  -t, --tag TEXT
  --help                          Show this message and exit.
```

## Arguments

`add` has only one required argument: `TASK`. `TASK` is a text containing some 
description of the task.

**Example:**
```console
$ timerdo add "<TASK>"
[17:21:34] Added a new entry with ID 21.
```
However, as you could see above in the `--help`, `add` has some options that are
not required but can be useful to better organize your to-do list.

## Options

`add` has four options. You can use them all together or in any combination. To call anyone, you must use the indicate before the input, with a short flag `-` or a long `--` one.

### Project

You can use `project` option to organize your tasks into different groups.
This is useful because Timerdo has some commands and reports to aggregate tasks
that have the same project name. `project` is a string.

If you set a `project` name and you have done all tasks related to it you cannot set a new task
with the same `project` name.

**Example:**

```console
$ timerdo add "<TASK>" --project "<PROJECT>"
[17:21:34] Added a new entry with ID 21.
```

### Due Date

You can also use `due-date` to set a due date for your task. Timerdo also has some features to use this information to your advantage, as we will see in the **list** and **reports**. `due-date` is a date with the following format.

**Example:**
```console
$ timerdo add "<TASK>" --due-date yyyy-mm-dd
[17:21:34] Added a new entry with ID 21.
```

### Reminder

`reminder` is also a date that you can use to hide a task until the reminder date.

**Example:**
```console
$ timerdo add "<TASK>" --reminder yyyy-mm-dd
[17:21:34] Added a new entry with ID 21.
```

### Status

`status` is automatically set to `to do` and as soon as you start a timer for the new task, the status will be updated to `doing`. Finally, when you complete any task, the status is also updated to `done`. However, you can also configure it manually.

`status` plays an important role in Timerdo because it defines which tasks are shown to you.

**Example:**
```console
$ timerdo add "<TASK>" --status "<[to do|doing|done]>"
[17:21:34] Added a new entry with ID 21.
```

### Tag

`tag` is also a way to organize your tasks into groups. It works similarly to `project`.

**Example:**
```console
$ timerdo add "<TASK>" --tag "<TAG>"
[17:21:34] Added a new entry with ID 21.
```


