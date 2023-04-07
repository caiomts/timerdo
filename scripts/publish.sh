#!/usr/bin/env bash

set -e

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/'

${PREFIX}python -m flit publish