# config/logging_config.py

import logging
import logging.config
import logging.handlers
from pathlib import Path
import os
import sys
from datetime import datetime
import traceback

# Set up the log directory based on date
LOG_DATE = datetime.now().strftime("%Y%m%d")
LOG_DIR = Path(__file__).parents[2] / "logs" / LOG_DATE
LOG_DIR.mkdir(parents=True, exist_ok=True)

# TODO: change your application name here
APP_NAME = os.getenv("APP_NAME", "Your App")


# Filter class for filtering info logs
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


# Formatter configurations
formatters = {
    "verbose": {
        "format": (
            "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
        ),
        "datefmt": "%Y-%m-%d %H:%M:%S",
    },
    "simple": {
        "format": "%(levelname)-8s %(message)s",
    },
}

# Filters
filters = {
    "info_filter": {
        "()": InfoFilter,
    }
}

# Handlers
handlers = {
    "console_info": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "INFO",
        "stream": sys.stdout,
        "filters": ["info_filter"],
    },
    "console_error": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "WARNING",
        "stream": sys.stderr,
    },
    "file_debug": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "formatter": "verbose",
        "level": "DEBUG",
        "filename": str(LOG_DIR / f"{APP_NAME}_debug.log"),
        "when": "midnight",
        "backupCount": 7,
        "encoding": "utf-8",
    },
    "file_error": {
        "class": "logging.handlers.RotatingFileHandler",
        "formatter": "verbose",
        "level": "WARNING",
        "filename": str(LOG_DIR / f"{APP_NAME}_errors.log"),
        "maxBytes": 5 * 1024 * 1024,  # 5 MB
        "backupCount": 7,
        "encoding": "utf-8",
    },
}

# Loggers per component
loggers = {
    "__main__": {
        "level": "DEBUG",
        "handlers": [
            "file_debug",
            "console_info",
            "console_error",
            "file_error",
        ],
        "propagate": False,
    }
}

# Complete config
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": formatters,
    "filters": filters,
    "handlers": handlers,
    "loggers": loggers,
    "root": {
        "level": "WARNING",
        "handlers": ["console_error", "file_error"],
    },
}


def setup_logging():
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
        logging.captureWarnings(True)

        logger = logging.getLogger(__name__)
        logger.info("=" * 80)
        logger.info(f"Initialized logging for {APP_NAME}")
        logger.info(f"Log directory: {LOG_DIR}")
        logger.info("=" * 80)

    except Exception as e:
        print(f"CRITICAL LOGGING ERROR: {e}")
        print(traceback.format_exc())
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(message)s",
            stream=sys.stdout,
        )
        fallback_logger = logging.getLogger(__name__)
        fallback_logger.error(
            "Failed to configure logging, using basic config"
        )
        fallback_logger.error(f"Error: {e}")
