import sys

from loguru import logger as _loguru_logger
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- GLOBAL & ENVIRONMENT VARIABLES
class ApplicationSettings(BaseSettings):
    """Configuration for stremio-addon-python-template.

    Values are read from environment variables and optionally
    overridden by a ``.env`` file.
    """

    # if .env is present, it will override the environment variables
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    HOST: str = Field(default="127.0.0.1", description="interface the server listens on")
    PORT: int = Field(default=7000, description="port the server listens on")
    ADDON_ID: str = Field(
        default="community.example.stremioaddonpythontemplate",
        description="unique addon id shown in the manifest",
    )

    logging_level: str = Field(
        default="DEBUG",
        validation_alias=AliasChoices("LOGGING_LEVEL", "logging_level"),
        description="Log level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )


def _initialize_logger(settings: ApplicationSettings):
    """Initialize the loguru logger with app-specific configuration."""
    level = settings.logging_level

    try:
        _loguru_logger.remove(0)
    except ValueError:
        pass

    _loguru_logger.add(
        sys.stderr,
        level=level,
        filter=lambda record: record["extra"].get("name") == "stremio_addon_python_template",
    )

    return _loguru_logger.bind(name="stremio_addon_python_template")


settings = ApplicationSettings()
logger = _initialize_logger(settings)
