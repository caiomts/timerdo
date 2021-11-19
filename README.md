![](images/timerdo.png)

Timerdo is a CLI app that manages a minimalist to-do list with built-in timer 
to track your work and keep you productive.


# Installation

![](images/pip_install.png)

Timerdo is 100% python, so pip installation should work regardless of your OS. 

*You may have to put it in the PATH to call it directly with the `timerdo` command.* 

# Quick Start

**Timerdo was thought to track tasks, so tasks are its building blocks. 
Keep it in mind.** 

**Done is Done. You can't do anything else with a task once it's done.**

## Add task
So, let's add your first:

![](images/add_1.png)

Task is a required argument, but you have some options. Let's take a look on it:

![](images/add_help.png)

So, you can also define a project to the task, but remember what I said? 
Tasks are the building block, so there is no project without a task!

In addition, you can set a due date for you task and a tag.

The reminder has a special feature. 
It will appear in your to-do list only after the defined day. 
This is for that type of task that you must do at a specific time or just remember it later.  

Finally, you can change the default status, but keep in mind. Done is Done.
You can visualize what was done, but that's it.

## Start the timer

Now that you already have a task, let's keep track of the time you spend on it.

![](images/start_1.png)

To start tracking the task ID is a required argument, 
I'll show you in a bit how to get to know the tasks IDs, but first let's have a look at the help.

![](images/start_help.png)

Nice, you can also set a *timebox* with the `--duration` flag! If you do so,
Timerdo keeps running and a message will pop up when you are done.

But How do I know my tasks IDs?!

## View

The Timerdo workflow was thought to keep things simple, so you add your tasks and
whenever you need to see your to-do list at the end of a task or at the start of your day
you simply call the view.

![](images/view.png)

This is the structure of the view, but Timerdo will show you only heads that
you have at least a task.

Let's see the help

![](images/view_help.png)

You can set until when it shows up the tasks with due dates. The default is
one week ahead.

## Stop

But let's stop our task!

![](images/stop_1.png)

Timerdo keep track of task status! So, whenever you start a task, if the status
is `to do`, Timerdo automatically changes it to `doing` and whenever you stop the timer
it ask you if you have finished the task. Cool, right?

*Timerdo don't let you work on a done task as well ;)*

As always, let's look at the help:

![](images/stop_help.png)

You can also write down some remarks to keep track of something important.
If you start a timer as a *timebox* this option will also be asked by the prompt.

# More features

Timerdo has more two modules.











