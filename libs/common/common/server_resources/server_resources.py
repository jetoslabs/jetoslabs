from typing import Optional

import aiohttp

from common.config.schemas.schema_config import Config


class ServerResources():
    """
    Act as ServerResources object store. Contains resources to be used by App server
    """

    def __init__(self):
        self.config: Optional[Config] = None
        self.http_client: Optional[aiohttp.ClientSession] = None

    async def close(self):
        if self.http_client:
            await self.http_client.close()

    def init_http_client(self):
        # TODO: Make this singleton thread/process safe
        if not self.http_client:
            self.http_client = aiohttp.ClientSession()
        return self.http_client
