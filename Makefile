# --- Portable Settings ---
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/Scripts/python.exe
PIP = $(VENV_DIR)/Scripts/pip.exe
KERNEL_NAME = your_notebook
NOTEBOOK_DIR = notebooks
SRC_DIR = src

# If on Unix-like system, override executables
ifeq ($(OS),)
	PYTHON = $(VENV_DIR)/bin/python
	PIP = $(VENV_DIR)/bin/pip
endif

.PHONY: help init install reset-kernel jupyter clean

help:
	@echo Available targets:
	@echo "  make init           Create virtual environment and install dependencies"
	@echo "  make install        Install project and dev tools"
	@echo "  make reset-kernel   Register Jupyter kernel for project"
	@echo "  make jupyter        Launch Jupyter Notebook"
	@echo "  make clean          Remove __pycache__ and checkpoints"

init:
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(MAKE) install

install:
	$(PIP) install -e .

reset-kernel:
	$(PYTHON) -m ipykernel install --user --name=$(KERNEL_NAME)

jupyter:
	cd $(NOTEBOOK_DIR) && $(PYTHON) -m notebook

clean:
	@echo Cleaning __pycache__ and .ipynb_checkpoints...
	-@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	-@for /d /r . %%d in (.ipynb_checkpoints) do @if exist "%%d" rmdir /s /q "%%d"