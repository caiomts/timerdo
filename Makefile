.PHONY: install format lint test sec

install:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements_dev.txt && python -m mkdocs new ./
format:
	@isort .
	@blue .
lint:
	@prospector --with-tool  pydocstyle --doc-warning
test:
	python test/run_before_tests.py
	python -m pytest -v
	python test/run_after_tests.py

