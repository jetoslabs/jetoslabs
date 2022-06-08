from functools import lru_cache
from web3 import Web3

from concepts.core.server_resources import server_resources


@lru_cache()
def get_w3_provider() -> Web3:
    # TODO: move config out of Server Resources
    uri = server_resources.config.SYSTEM.web3.provider_uri
    return Web3(Web3.HTTPProvider(uri))


