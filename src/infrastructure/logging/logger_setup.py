import logging
import logging.config
import sys
from config.config import config


def setup_logger():
    log_level = config.log_level.upper()
    log_file = "app.log"

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            },
            "colored": {
                "()": "uvicorn.logging.ColourizedFormatter",
                "format": "%(levelprefix)s [%(name)s]: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": log_level,
                "stream": sys.stderr,  # uvicorn использует stderr
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "maxBytes": 5_000_000,
                "backupCount": 3,
                "formatter": "default",
                "level": log_level,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": log_level,
        },
        # Настройки для конкретных логгеров
        "loggers": {
            "src": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "config": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(log_config)
    
    # Добавляем тестовое сообщение для проверки работы логгера
    logging.getLogger("src.infrastructure.logging").info("Logging system initialized")