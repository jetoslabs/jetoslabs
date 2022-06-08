from typing import Tuple

import aiohttp
import loguru
from aiohttp import ClientResponse

from common.decorators.retry import retry


async def ping_google(http_client: aiohttp.ClientSession, *, logger: loguru.logger) -> Tuple[ClientResponse, str]:
    @retry(times=3, logger=logger)
    async def ping():
        async with http_client.get("https://www.google.com") as resp:
            return resp, await resp.text()
    return await ping()
