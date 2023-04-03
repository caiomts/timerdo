#!/usr/bin/env bash

PREFIX=''

[[ -z "$GITHUB_ACTIONS" ]] && PREFIX='.venv/bin/' && python -m venv .venv 

${PREFIX}python -m pip install --upgrade pip flit
${PREFIX}python -m flit install --symlink --deps all