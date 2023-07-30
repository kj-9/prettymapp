SHELL=/bin/bash

.PHONY:
	pip-upgrade
	test
	test[live]
	pre-commit
	setup
	setup-dev
	package
	upload
	clean

pip-upgrade:
	python -m pip install --upgrade pip

test:
	-rm -r .pytest_cache
	python -m pytest -vv --durations=3

test[live]:
	-rm -r .pytest_cache
	python -m pytest -vv --runlive --durations=5

pre-commit:
	pre-commit run --all-files --show-diff-on-failure

setup:
	pip install -e .

setup-dev:
	pip install -e '.[test]'
	pip install streamlit

package:
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install build twine
	python -m pip list
	python -m build --outdir dist/ .

upload:
	twine upload --skip-existing dist/*

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -exec rm -f {} +
