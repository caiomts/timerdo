#!/usr/bin/env bash

set -e

PREFIX=''

export TIMERDOTEST='./'

[[ -d .venv ]] && PREFIX='.venv/bin/' && python -m venv .venv

${PREFIX}python scripts/docs_db.py
${PREFIX}timerdo report

rm -rf TimerdoTest/