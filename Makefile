SHELL := /bin/bash

init:
	python3 -m venv cyberguard_venv; \
	source cyberguard_venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements/requirements.txt
