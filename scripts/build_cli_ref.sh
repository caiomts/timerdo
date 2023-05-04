#!/usr/bin/env bash

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/'

${PREFIX}typer timerdo.main utils docs --name timerdo --output ./docs/cli_reference.md