.PHONY: bootstrap format tests build_ref docs

VPATH = timerdo:test

bootstrap:
	bash scripts/bootstrap.sh

format:
	bash scripts/format.sh

tests:
	bash scripts/tests.sh

docs:
	bash scripts/docs_preview.sh

build_ref:
	bash scripts/build_cli_ref.sh

docs_shot:
	bash scripts/gen_docs_db.sh
