.PHONY: setup install format tests

VPATH = timerdo:test

setup:
	python -m venv .venv
	python -m pip install -U pip flit

install:
	python -m flit install --symlink --deps all

format:
	. scripts/format.sh

tests:
	. scripts/tests.sh
