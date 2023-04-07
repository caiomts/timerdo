#!/usr/bin/env bash

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/'

[[ -d docs ]] ||  ${PREFIX}python -m mkdocs new .

${PREFIX}typer timerdo.main utils docs --name timerdo --output ./docs/cli_reference.md
${PREFIX}python -m mkdocs serve
