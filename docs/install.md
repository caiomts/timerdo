# Installing Timerdo
Timerdo is a CLI application 100% written in Python. So, if you're a Python user, you can easily install Timerdo.


### with pipx <small>recommended</small>

```shell
$ pipx install timerdo
```

If you've never used [pipx][^1] before, do yourself a favor and just install it :teacher:. 

### with pip

```shell
$ pip install timerdo
```

If you already tried [pipx] but somehow don't like it you can 
stick with the classic `pip install`.

### verifying Your Installation

```shell
$ timerdo
╭───────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│ Timerdo is a minimalist to-do list with built-in timer to keep your tasks on track.       │
│                                                                                           │
│ To get started call `$ timerdo --help` or read the documentation at                       │
│ https://caiomts.github.io/timerdo/                                                        │
│                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

If your output is similar to the one highlighted above, you're good :rocket:.

If not, you may have an older version. Let's try this:

```shell hl_lines="2"
$ timerdo --version
Timerdo version: 0.0.4
```

If you have an older version, just follow along.

## Upgrading Timerdo

### with pipx <small>recommended</small>

```shell
$ pipx upgrade timerdo
```

### with pip

```shell
$ pip install --upgrade timerdo
```

Now that everything is up and running, you can get started with Timerdo by moving on to
the next section.

[tutorial]:tutorials.md
[pipx]:https://pypa.github.io/pipx/
[^1]: Pipx installs CLI apps in isolated environments and exposes the
entry points to your `PATH` so you can call them directly with no concerns
if you are in the right python env or not, without dependency conflicts and clean uninstalls :sweat_smile:.
