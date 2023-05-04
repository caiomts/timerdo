#!/usr/bin/env bash

set -e
set -x

PREFIX=''

export TIMERDOTEST='./'

[[ -d .venv ]] && PREFIX='.venv/bin/' && python -m venv .venv

${PREFIX}python -m pytest --cov-fail-under=95 \
    --cov-config=.coveragerc \
    --cov-report \
    term-missing \
    --cov=timerdo test/

