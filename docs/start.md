# Getting Started

!!! warning
    Making sure you have Timerdo entry point in your `PATH`. If you are not sure,
    go back to [installing Timerdo](install.md#installing-timerdo). 

## Adding Your First Task

The very first step when you start using Timerdo is to write down your tasks and
it's simple as:

```shell
$ timerdo task "<your task goes here>"
```
Timerdo runs silently. No return is a good return. 
Your first task will get `id = 1`, the next one `id = 2` and so on...

I'll show you in a bit how to retrieve your tasks. But let's first work on
in your first task.

## Starting The Timer

To start a timer you need just your task id. Let's say your `id` is 1, as you're
starting a timer for the first task you've just written to your to do list.

```shell
$ timerdo start 1
```
Again, no return is a good return. The timer is now running. Let's say you've just
finished your task for now. 

## Stopping The Timer

To stop the timer you don't need any information, Timerdo already knows what to do.
I mean, Timerdo almost know what to do. It will raise a question about whether or note the task is done.

```shell
$ timerdo stop
Done [y/n]: n
```
No return. You already know... 

??? info
    We already know that Timerdo runs silently, but let's see what happens if something
    goes wrong. Let's say you don't know you stopped the timer or not and you try to stop
    it again:
    
    ```shell
    $ timerdo stop
    Done [y/n]: n
    💥️ No timer running.
    ```
    Timerdo try to catch errors and exceptions and only gives you back a useful message.


## Reporting your tasks

Now that you already know how Timerdo works, let's see how you can read your data.

```shell hl_lines="4 7" linenums="1"
$ timerdo report

                                                                                             
                                                             from 1789-07-14 until 2023-05-04
                                                                                             

                    🏷️      ---   0 days 00:04:08                    
                                                                    
╭────┬────────────┬───────────────────────┬──────────┬────────┬─────────────────╮
│ ID │       Date │ Task                  │ Deadline │ Status │      Time       │
├────┼────────────┼───────────────────────┼──────────┼────────┼─────────────────┤
│  1 │ 2023-05-04 │ <your task goes here> │          │ Doing  │ 0 days 00:04:08 │
╰────┴────────────┴───────────────────────┴──────────┴────────┴─────────────────╯

```

??? info
    In real life the returns are much prettier as you can see in the example below.
    However, I prefer keep it as simple as code blocks and not clutter too much the documentation.
    ![timerdo_report](img/screenshot_timerdo_report.png)

### Digging into the report

Let's start by the highlights outside the table. the line 4 show us the period of timers
Timerdo took into account to aggregate times. which means that all timers between those dates
were considered in the report.

The 🏷️ in line 7 is a tag mark. You can tag your tasks and when
Timerdo report them it will break the report down per tags given, also giving you the time
spent per tag. You can also filter which tags you are interested in :exploding_head:.

In the table header you have two more information: *Deadline* and *Status*. *Deadline* is empty,
but *Status* is always defaults to *To Do* when you create a new task and changes to *Doing* when you start the timer for the first time.

Now that you know the basics, you can start using Timerdo. 
However, Timerdo has more features that you might already be missing.
Let's dig into all this functionalities in the next section.

