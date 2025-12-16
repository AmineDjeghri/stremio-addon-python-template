# Initialize settings and configure logging
from stremio_addon_python_template.env_settings import Settings

import sys

from loguru import logger as loguru_logger

if "stremio-addon-python-template" not in os.getcwd().split(os.sep)[-1]:  
    raise Exception(f"Please run the library from the root directory. Current directory: {os.getcwd()}")

def initialize():
    settings = Settings()
    loguru_logger.remove()

    if settings.DEV_MODE:
        loguru_logger.add(sys.stderr, level="TRACE")
    else:
        loguru_logger.add(sys.stderr, level="INFO")

    return settings, loguru_logger


settings, logger = initialize()


def hello():
    logger.info("Hello World")


# Get version from pyproject.toml
from importlib.metadata import version

__version__ = version("stremio-python-addon-template")
