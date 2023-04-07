#!/usr/bin/env bash

set -e

PREFIX=''

[[ -d .venv ]] && ( 
    PREFIX='.venv/bin/' && [[ ./docs/cli_reference.md -nt ./timerdo/main.py ]] || ( 
    echo "CLI ref is outdated" && exit 1 ) 
)

${PREFIX}python -m black timerdo/ test/
${PREFIX}python -m pydocstyle timerdo/
${PREFIX}python -m isort timerdo/ test/
${PREFIX}python -m flake8 timerdo/ test/

