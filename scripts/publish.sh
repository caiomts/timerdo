#!/usr/bin/env bash

PREFIX=''

[[ -d .venv ]] && PREFIX='.venv/bin/' && python -m venv .venv