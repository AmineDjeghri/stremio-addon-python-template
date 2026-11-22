import importlib

import pytest


@pytest.fixture
def settings_module(tmp_path, monkeypatch):
    """Import settings away from local credentials and isolate logging overrides."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOGGING_LEVEL", raising=False)
    monkeypatch.delenv("logging_level", raising=False)
    return importlib.import_module("stremio_addon_python_template.settings")


def test_settings(settings_module):
    """Test that ApplicationSettings can be instantiated."""
    settings = settings_module.ApplicationSettings(_env_file=None)
    assert settings is not None


def test_logging_level_default(settings_module):
    """Test that logging_level defaults to DEBUG."""
    settings = settings_module.ApplicationSettings(_env_file=None)
    assert settings.logging_level == "DEBUG"


def test_logging_level_from_env(monkeypatch, settings_module):
    """Test that LOGGING_LEVEL can be set from environment variable."""
    monkeypatch.setenv("LOGGING_LEVEL", "INFO")
    settings = settings_module.ApplicationSettings(_env_file=None)
    assert settings.logging_level == "INFO"


def test_initialize_logger(settings_module):
    """Test that _initialize_logger returns a loguru logger bound to the app namespace."""
    settings = settings_module.ApplicationSettings(_env_file=None)
    logger = settings_module._initialize_logger(settings)
    assert logger is not None
    assert hasattr(logger, "debug")
    assert hasattr(logger, "info")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")


def test_addon_defaults(monkeypatch, settings_module):
    """Test that the server listens locally by default."""
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    settings = settings_module.ApplicationSettings(_env_file=None)
    assert (settings.HOST, settings.PORT) == ("127.0.0.1", 7000)
