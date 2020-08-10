PIP := pip install --upgrade

tests:
	@pylint --disable=C *py zerocue
	@pytest tests*py

dependencies: install-pylint install-pytest

install-pylint:
	@$(PIP) pylint

install-pytest:
	@$(PIP) pytest

install-venv:
	@python3 -m venv .env

# https://packaging.python.org/tutorials/packaging-projects/
build: tests
	@$(PIP) setuptools wheel
	@python3 setup.py sdist bdist_wheel

upload: build
	@$(PIP) twine
	@python3 -m twine upload dist/*

.PHONY: tests dependencies install-pylint install-pytest install-venv build upload
