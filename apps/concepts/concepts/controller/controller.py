from typing import Tuple

import loguru
from aiohttp import ClientResponse

from concepts.core.server_resources import server_resources
from common.decorators.retry import retry


async def ping_google(*, logger: loguru.logger) -> Tuple[ClientResponse, str]:
    @retry(times=3, logger=logger)
    async def ping():
        async with server_resources.http_client.get("https://www.google.com") as resp:
            return resp, await resp.text()
    return await ping()
