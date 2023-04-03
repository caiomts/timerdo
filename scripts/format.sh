#!/usr/bin/env bash

set -e

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/'

${PREFIX}python -m flake8 timerdo/ test/
${PREFIX}python -m isort timerdo/ test/
${PREFIX}python -m pydocstyle timerdo/
${PREFIX}python -m black timerdo/ test/
