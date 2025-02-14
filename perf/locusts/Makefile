VENV_DIR := .venv
HOST ?= http://127.0.0.1:5000

install:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install uv && uv sync

start:
	$(MAKE) install
	. $(VENV_DIR)/bin/activate && locust -f src/ft.py --host=$(HOST)

start-local:
	$(MAKE) start HOST=http://127.0.0.1:5000

start-prod:
	$(MAKE) start HOST=https://pa-back-prod-test.osc-secnum-fr1.scalingo.io
