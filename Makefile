# --- Portable Settings ---
VENV_DIR = .venv
KERNEL_NAME = your_notebook
NOTEBOOK_DIR = notebooks
SRC_DIR = src

# Detect operating system
ifeq ($(OS),Windows_NT)
	# Windows (including PowerShell)
	PYTHON = $(VENV_DIR)/Scripts/python.exe
	PIP = $(VENV_DIR)/Scripts/pip.exe
	RM_RF = if exist "$1" rmdir /s /q "$1"
	MKDIR = if not exist "$1" mkdir "$1"
	SHELL = cmd
else
	# Unix-like systems (Linux, macOS, WSL)
	PYTHON = $(VENV_DIR)/bin/python
	PIP = $(VENV_DIR)/bin/pip
	RM_RF = rm -rf $1
	MKDIR = mkdir -p $1
endif

.PHONY: help init install reset-kernel clean test format

help:
	@echo Available targets:
	@echo "  make init           Create virtual environment and install dependencies"
	@echo "  make install        Install project and dev tools"
	@echo "  make format         Format code with black"
	@echo "  make test           Run tests"
	@echo "  make clean          Remove __pycache__ and checkpoints"

init:
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(MAKE) install

install:
	$(PIP) install -e

init-dev:
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -e .[dev]

reset-kernel:
	$(PYTHON) -m ipykernel install --user --name=$(KERNEL_NAME) --display-name="$(KERNEL_NAME)"

format: init-dev
	$(PYTHON) -m black $(SRC_DIR)
	$(PYTHON) -m black $(NOTEBOOK_DIR) --ipynb

test:
	$(PYTHON) -m pytest tests/ -v

clean:
	@echo Cleaning __pycache__ and .ipynb_checkpoints...
	ifeq ($(OS),Windows_NT)
		@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul || echo.
		@for /d /r . %%d in (.ipynb_checkpoints) do @if exist "%%d" rmdir /s /q "%%d" 2>nul || echo.
		@del /s /q *.pyc 2>nul || echo.
	else
		@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
		@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
		@find . -name "*.pyc" -delete 2>/dev/null || true
	endif