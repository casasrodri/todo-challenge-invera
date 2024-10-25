import os
from .utils import get_base_dir

# Set directories
BASE_DIR = get_base_dir()
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Environment variables
LOG_REQUEST_RESPONSE = os.getenv("LOG_REQUEST_RESPONSE") == "True"
LOG_REQUEST_RESPONSE_LEVEL = os.getenv("LOG_REQUEST_RESPONSE_LEVEL", "INFO")
LOG_REQUEST_RESPONSE_CONSOLE = os.getenv("LOG_REQUEST_RESPONSE_CONSOLE") == "True"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "requests": {
            "format": "{asctime}\t{levelname}\t{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/errors.log",
            "formatter": "verbose",
        },
        "request_response_file": {
            "level": LOG_REQUEST_RESPONSE_LEVEL,
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/requests.log",
            "formatter": "requests",
        },
    },
    "loggers": {
        # Standard Django loggers
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "rest_framework": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

if LOG_REQUEST_RESPONSE:
    LOGGING["loggers"]["request_response"] = {
        "handlers": ["request_response_file"],
        "level": LOG_REQUEST_RESPONSE_LEVEL,
        "propagate": True,
    }

    if LOG_REQUEST_RESPONSE_CONSOLE:
        LOGGING["loggers"]["request_response"]["handlers"].append("console")
