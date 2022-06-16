from functools import lru_cache

from fastapi.security import OAuth2PasswordBearer, APIKeyHeader, APIKeyCookie
import aiohttp
import ipfshttpclient
from fastapi import HTTPException, Security
from starlette import status
from web3 import Web3

from common.auth.constants import TOKEN_TYPE_BEARER
from common.users.user import User, fake_users_db, get_user_from_token
from concepts.core.resources import server_resources
from concepts.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/user/token")

API_KEY = "access_token"
api_key_header_scheme = APIKeyHeader(name=API_KEY, auto_error=False)
api_key_cookie_scheme = APIKeyCookie(name=API_KEY, auto_error=False)


def get_current_user(token: str = Security(oauth2_scheme)) -> User:
    return get_user_from_token(settings.SECRET_KEY, settings.ALGORITHM, token)


def get_current_active_user(current_user: User = Security(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user


def get_current_active_admin_user(current_user: User = Security(get_current_active_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Non-Admin User")
    return current_user


def get_current_user_from_api_key(
        api_key_header: str = Security(api_key_header_scheme),
        api_key_cookie: str = Security(api_key_cookie_scheme)
) -> User:
    api_key: str | None = None
    if api_key_header: api_key = api_key_header
    if api_key_cookie: api_key = api_key_cookie
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    token_type, token = api_key_cookie.split(' ')
    if token_type != TOKEN_TYPE_BEARER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return get_user_from_token(settings.SECRET_KEY, settings.ALGORITHM, token)


def get_current_active_user_from_api_key(
        api_key_header: str = Security(api_key_header_scheme),
        api_key_cookie: str = Security(api_key_cookie_scheme)
) -> User:
    current_user: User = get_current_user_from_api_key(api_key_header, api_key_cookie)
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user


def get_current_active_admin_user_from_api_key(
        api_key_header: str = Security(api_key_header_scheme),
        api_key_cookie: str = Security(api_key_cookie_scheme)
) -> User:
    current_user: User = get_current_user_from_api_key(api_key_header, api_key_cookie)
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Non-Admin User")
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
