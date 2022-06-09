from typing import Optional

import aiohttp
from web3 import Web3

from common.config.schemas.schema_config import Config


class ServerResources():
    """
    Act as ServerResources object store. Contains resources to be used by App server
    """

    def __init__(self):
        self.config: Optional[Config] = None
        self.http_client: Optional[aiohttp.ClientSession] = None
        # TODO: create Resource Type (mirror of config but LazyVar and initialized based on config)
        # TODO: move web3_provider in Resource.system_resource.web3_provider
        self.web3_provider: Optional[Web3] = None

    async def close(self):
        if self.http_client:
            await self.http_client.close()

    def init_http_client(self):
        # TODO: Make this singleton thread/process safe
        if not self.http_client:
            self.http_client = aiohttp.ClientSession()
        return self.http_client


# Note: Create server resources here and not in main
# as Creating server resources here will cause import cycle issues
# (as server resources is being used everywhere and will import from main file)
def create_server_resources() -> ServerResources:
    server_resources = ServerResources()
    return server_resources


server_resources: ServerResources = create_server_resources()
