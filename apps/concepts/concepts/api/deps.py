from functools import lru_cache

import aiohttp
import ipfshttpclient
from fastapi import HTTPException
from starlette import status
from web3 import Web3

from concepts.core.resources import server_resources


@lru_cache()
def get_w3_provider() -> Web3:
    provider = server_resources.get_web3_provider()
    if not provider:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="web3 provider is not available")
    return provider


async def get_http_client() -> aiohttp.ClientSession:
    client = await server_resources.get_http_client()
    if not client:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="http client is not available")
    return client


def get_ipfs_client() -> ipfshttpclient.Client:
    client = server_resources.get_ipfs_client()
    if not client:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ipfs client is not available")
    return client
