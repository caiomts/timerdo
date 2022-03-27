# Start

`start` starts the timer.

```console
$ timerdo start --help
Usage: timerdo start [OPTIONS] TASK_ID

  Start Timer for a given open task.

Arguments:
  TASK_ID  [required]

Options:
  -d, --duration INTEGER  Duration in minutes
  --help                  Show this message and exit.
```

## Arguments

`start` has only one required argument: `TASK_ID`. `TASK_ID` is the *ID* of the task you
are starting the timer on. You can easily access the *ID's* using the `list` command.

**Example:**
```console
$ timerdo start <ID>
[19:09:38] <TASK>. Timer id: 18
```

## Options

`start` has only one option: `duration`

### Duration

`duration` triggers a timer with a given duration.

**Example:**

```console
$ timerdo start 12 --duration <MINUTES>
[19:15:00] <TASK> has just started. Timer id: <TIMER ID>                        
⠙ Working ━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  <%> <REMINDER DURATION>
```
You can *stop* or *abort* the process at any time, but be careful because **you will
need to stop the timer** anyway using `stop` from Timerdo.
