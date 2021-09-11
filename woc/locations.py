import os

from pathlib import Path

from .utils.appdirs import user_cache_dir
from .utils.appdirs import user_config_dir
from .utils.appdirs import user_data_dir

CACHE_DIR = user_cache_dir("woc")
DATA_DIR = user_data_dir("woc")
CONFIG_DIR = user_config_dir("woc")

REPOSITORY_CACHE_DIR = Path(CACHE_DIR) / "cache" / "repositories"


def data_dir() -> Path:
    if os.getenv("WOC_HOME"):
        return Path(os.getenv("WOC_HOME")).expanduser()

    return Path(user_data_dir("woc", roaming=True))
