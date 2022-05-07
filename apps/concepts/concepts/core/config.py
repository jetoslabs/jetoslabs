from concepts.core.settings import settings
from common.config.config import load_config_folder


def setup_config():
    config = load_config_folder(settings.CONFIGURATION_LOC)
    print(config)
    return config
