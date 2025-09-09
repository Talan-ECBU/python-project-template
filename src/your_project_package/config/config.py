# config/config.py
"""Configuration file for the project."""

import logging.config
from datetime import datetime
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = Path(__file__).resolve().parent

with open(CONFIG_DIR / "filepaths.yaml") as yaml_file:
    FILEPATHS = yaml.safe_load(yaml_file)


def get_filepath(*groupings) -> Path:
    """Get the full path for a given data groupings."""
    first_level = FILEPATHS.get(groupings[0], {})
    if not first_level:
        raise ValueError(f"Invalid grouping: {groupings[0]}")
    current_level = first_level
    for grouping in groupings[1:]:
        current_level = current_level.get(grouping, {})
        if not current_level:
            raise ValueError(f"Invalid grouping: {grouping}")
        if isinstance(current_level, str):
            return PROJECT_ROOT / Path(current_level)


def setup_logging():
    """Load logging configuration from YAML file."""
    with open(PACKAGE_ROOT / "config" / "logging_config.yaml") as f:
        config = yaml.safe_load(f)
    current_date = datetime.now().strftime("%Y%m%d")

    for _, handler_config in config.get("handlers", {}).items():
        if "filename" in handler_config:
            filename = handler_config["filename"]
            if not Path(filename).is_absolute():
                log_path = Path(filename)
                date_based_path = log_path.parent / current_date / log_path.name
                full_path = PROJECT_ROOT / date_based_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                handler_config["filename"] = str(full_path)

    logging.config.dictConfig(config)



