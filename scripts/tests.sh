#!/usr/bin/env bash

set -e

[[ -d .venv ]] && export PREFIX='.venv/bin' || export PREFIX=''

${prefix}python -m pytest --cov-report term-missing --cov=timerdo test/