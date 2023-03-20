.PHONY: bootstrap format tests build docs

VPATH = timerdo:test

bootstrap:
	bash scripts/bootstrap.sh

format:
	bash scripts/format.sh

tests:
	bash scripts/tests.sh
