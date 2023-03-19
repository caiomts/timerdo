.PHONY: setup install format tests

VPATH = timerdo:test

setup:
	python -m venv .venv && \
	. .venv/bin/activate && \
	python -m pip install -U pip flit

install:
	. .venv/bin/activate && \
	python -m flit install --symlink --deps all

format:
	bash scripts/format.sh

tests:
	bash scripts/tests.sh
