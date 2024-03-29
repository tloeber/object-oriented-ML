SHELL := /bin/bash

setup:
	@# Install Poetry into base environment, if not already present
	(python3 -m poetry --version > /dev/null) || pip3 install poetry

	@# Note: Poetry creates *editable* install for root project by default
	python3 -m poetry install --all-extras

	@echo ""
	@echo "Please manually set this environment as default in IDE for this project."
	@echo "E.g., in the VSCode workspace file, add the following line:"
	@echo "\"settings\": {\"python.defaultInterpreterPath\": \"$(python3 -m poetry env info --executable)\"}"
	@echo "(This way you don't have to manually activate it for each shell using `python3 -m poetry shell`)"

update:
	python3 -m poetry update

test:
	poetry run pytest

build:
	poetry build

publish:
	poetry publish
