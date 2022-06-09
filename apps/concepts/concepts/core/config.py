import loguru

from common.config.config import load_config_folder
from common.settings.settings import Settings


def setup_config(settings: Settings):
    config = load_config_folder(settings.CONFIGURATION_LOC)
    loguru.logger.bind(config=config).info("Config loaded")
    return config
