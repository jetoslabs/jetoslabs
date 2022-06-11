from typing import Optional

import aiohttp
from ipfshttpclient import Client as IPFSClient
from web3 import Web3

from common.config.schemas.schema_config import Config
from common.ipfs_client.ipfs_client import close_ipfs_client, new_ipfs_client
from common.settings.settings import Settings
from common.web3_client.web3_provider import new_w3_provider
from concepts.core.config import setup_config


class ServerResources():
    """
    Act as ServerResources object store. Contains resources to be used by App server
    """

    def __init__(self):
        self._config: Optional[Config] = None
        self._http_client: Optional[aiohttp.ClientSession] = None
        # TODO: create Resource Type (mirror of config but LazyVar and initialized based on config)
        # TODO: move web3_provider in Resource.system_resource.web3_provider
        self._web3_provider: Optional[Web3] = None
        self._ipfs_client: Optional[IPFSClient] = None

    def setup_server_resources(self, settings: Settings):
        """
        Setup necessary vars, others vars are supposed to be lazy vars
        :param settings:
        :return:
        """
        # First setup config
        self._config = setup_config(settings)
        # # setup http_client
        # self.get_http_client()

    async def close(self):
        if self._http_client:
            await self._http_client.close()
        if self._ipfs_client:
            await close_ipfs_client(self._ipfs_client)

    def get_config(self):
        return self._config

    async def get_http_client(self):
        # TODO: Make this singleton thread/process safe, functools - lru_cache
        # lazy eval
        if not self._http_client:
            async def get_client():
                # if aiohttp.ClientSession() is called directly it will not be a async func
                # and so will not have a loop and will cause error
                return aiohttp.ClientSession()
            self._http_client = await get_client()
        return self._http_client

    def get_web3_provider(self):
        # lazy eval
        if not self._web3_provider:
            self._web3_provider = new_w3_provider(self._config.SYSTEM.web3.provider_uri)
        return self._web3_provider

    def get_ipfs_client(self):
        # lazy eval
        if not self._ipfs_client:
            self._ipfs_client = new_ipfs_client()
        return self._ipfs_client


# Note: Create server resources here and not in main
# as Creating server resources here will cause import cycle issues
# (as server resources is being used everywhere and will import from main file)
def create_server_resources() -> ServerResources:
    resources = ServerResources()
    return resources


server_resources: ServerResources = create_server_resources()
