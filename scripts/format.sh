#!/usr/bin/env bash

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/' && python -m venv .venv

${PREFIX}python -m flake8 \
    --extend-ignore=E203,E711,E712 \
    --max-line-length=79 \
    --exclude=__init__.py \
    --max-complexity=10 \
    timerdo test
${PREFIX}python -m isort timerdo test
${PREFIX}python -m black timerdo test