from functools import lru_cache

from fastapi.security import OAuth2PasswordBearer
import aiohttp
import ipfshttpclient
from fastapi import HTTPException, Depends
from starlette import status
from web3 import Web3

from common.users.user import User, fake_users_db, get_current_user_from_token
from concepts.core.resources import server_resources

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/user/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return get_current_user_from_token(token)


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user


def get_fake_db():
    return fake_users_db


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
    try:
        client = server_resources.get_ipfs_client()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ipfs client is not available, e = {e}"
        )
    return client
