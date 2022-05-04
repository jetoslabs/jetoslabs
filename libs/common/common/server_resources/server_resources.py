from typing import Optional

import aiohttp


class ServerResources():

    def __init__(self):
        self.http_client: Optional[aiohttp.ClientSession] = None

    async def close(self):
        if self.http_client:
            await self.http_client.close()

    def init_http_client(self):
        self.http_client = aiohttp.ClientSession()
