#!/usr/bin/env bash

PREFIX=''

[[ -z "$GITHUB_ACTIONS" ]] || ${PREFIX}mkdocs gh-deploy --force





