"""
Configuration module for the application.
Loads and validates configuration from TOML files.
"""

# ----- Imports -----
from dynaconf import Dynaconf
from adaptix import Retort
from src.config_schema import Config


# ----- Configuration Loading -----
retort = Retort()

config: Config = retort.load(
    Dynaconf(
        settings_files=["./config/config.toml", "./config/secret.toml"],
        merge_enabled=True,
        environments=True
    ),
    Config
)
