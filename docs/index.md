# Timerdo

![Logo](img/logo.png){ width="400" }

A minimalist to-do list with built-in timer to keep your tasks on track. 

Timerdo is an intuitive CLI application that will help you focus on what really matters.

---
## Requirements

Python 3.10+

No fear of the command-line interface :laughing:.

--

**Source Code:** https://github.com/caiomts/timerdo  

**Documentation:** http://caiomts.github.io/timerdo

:warning: Early stage project[^2]

---

## Getting started
Timerdo is a CLI application 100% written in Python. So, if you're a Python user, you can easily install Timerdo with `pip[x]`. If you not, don't be afraid, follow along with the [tutorial] and start using python :partying_face:.

### Install Timerdo

#### with pipx <small>recommended</small>

```shell
$ pipx install timerdo
```

If you've never used [pipx][^1] before, do yourself a favor and just install it :teacher:. 

#### with pip

```shell
$ pip install timerdo
```

If you already tried [pipx] but somehow don't like it you can 
stick with the classic `pip install`.

#### verifying your installation

```shell hl_lines="2"
$ timerdo
timerdo Version: 0.0.3
```

If your output is similar to the one highlighted above, you're good :rocket:.

### Adding your first task

```shell
$ timerdo task "<your task goes here>"
```
No return. No problem :smile:.

### Starting the timer

```shell
$ timerdo start <your task id>
```
No return. No problem.

### Stopping the timer

```shell
$ timerdo stop
```
No return. you already know...

### Getting task IDs

```shell
$ timerdo query sql
[
    (3, 'Team Eight Group Receive Even Option Investment.', None, None, 'To Do', None),
    (4 'Clearly Whom Win Go Score World.', None, None, 'To Do', None),
    (5, 'Hand Style Manager Strong Enter Lot Federal Individual.', None, None, 'To Do', 
None),
    (6, 'Action Society Whose Sport Tv Over West.', None, None, 'Doing', 6),
    (7, 'Pressure Character Plan Almost Watch Compare Record.', None, None, 'Doing', 0),
    (8, 'Stage Require Mind Way Sit Ahead Watch Ten.', None, None, 'To Do', None),
    (9, 'Fall Administration Moment.', None, None, 'To Do', None),
    (1, 'Team Eight Group Receive Even Option Investment.', 'Moon', '2023-03-01', 'Doing', 1),
    (2, 'Action Society Whose Sport Tv Over West.', None, '2023-03-02', 'To Do', None)
]

```

??? warning "Under construction :factory_worker:" 
    Up to this point you have a query with all your tasks and the minutes you spent in each one of them.

    These are the planned steps:

    - [x] Core function to query database using text (SQLite queries).
    - [x] CLI function to [rich](https://rich.readthedocs.io/en/latest/)-print query results.
        * [ ] Print tables as result.
    - [ ] Create config file where users can create and persist
    their own queries.
    - [ ] Create class to handle queries and generate tables to print.

!!! example
    | id | task | tag | deadline | status | Time (min)|
    |:--:|:----:|:---:|:--------:|:------:|:---------:|
    |1|Team Eight Group Receive Even Option Investment|Moon|2023-03-01|Doing|1|


If you already have your Timerdo installed and are wondering how to do things, my suggestion is to go directly to the [How-to guides](/how_to_guides/) section.


[tutorial]:tutorials.md
[pipx]:https://pypa.github.io/pipx/
[^1]: Pipx installs CLI apps in isolated environments and exposes the
entry points to your `PATH` so you can call them directly with no concerns
if you are in the right python env or not, without dependency conflicts and clean uninstalls :sweat_smile:.
[^2]: Data models are mostly stable, but visualization and queries are in full development and the API can change quickly.
