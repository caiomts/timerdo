#!/usr/bin/env bash

set -e
set -x

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/' && python -m venv .venv

${PREFIX}python -m pytest --cov-fail-under=95 --cov-report term-missing --cov=timerdo test/