# config/config.py
"""Configuration file for the project."""

# External imports
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
CONFIG_DIR = SRC_DIR / "config"
