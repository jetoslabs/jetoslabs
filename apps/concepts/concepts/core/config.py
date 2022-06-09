import loguru

from common.config.config import load_config_folder
from concepts.core.settings import settings


def setup_config():
    config = load_config_folder(settings.CONFIGURATION_LOC)
    loguru.logger.bind(config=config).info("Config loaded")
    return config
