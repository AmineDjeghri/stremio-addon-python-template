# Initialize settings and configure logging
from stremio_addon_python_template.env_settings import Settings

import sys

from loguru import logger as loguru_logger


def initialize():
    settings = Settings()
    loguru_logger.remove()

    if settings.DEV_MODE:
        loguru_logger.add(sys.stderr, level="TRACE")
    else:
        loguru_logger.add(sys.stderr, level="INFO")

    return settings, loguru_logger


settings, logger = initialize()
