from common.config.schemas.schema_config import Config
from common.web3_client.web3_provider import get_w3_provider


def setup_web3_provider(config: Config):
    return get_w3_provider(config.SYSTEM.web3.provider_uri)
