from functools import lru_cache

import aiohttp
from fastapi import HTTPException
from starlette import status
from web3 import Web3

from concepts.core.resources import server_resources


@lru_cache()
def get_w3_provider() -> Web3:
    if not server_resources.web3_provider:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="web3 provider is not available")
    return server_resources.web3_provider


def get_http_client() -> aiohttp.ClientSession:
    if not server_resources.http_client:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="http client is not available")
    return server_resources.http_client

