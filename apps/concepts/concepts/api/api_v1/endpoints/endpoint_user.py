from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from fastapi.responses import Response
from fastapi.requests import Request

from common.auth.constants import TOKEN_TYPE_BEARER
from common.users.schemas import User, UserInDB
from common.auth.tokenizing import Token
from common.users.user import authenticate_user, create_user_access_token
from concepts.api.deps import get_fake_db, get_current_active_user, get_current_user_from_api_key
from concepts.core.settings import settings

router = APIRouter()


@router.post("/token")
async def post_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Authenticate for username and password and then generate and return token for the username
    :param form_data:
    :return:
    """
    user_in_db: UserInDB | bool = authenticate_user(get_fake_db(), form_data.username, form_data.password)
    if not isinstance(user_in_db, UserInDB):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    expire_delta = timedelta(minutes=15)
    data_dict: dict = User(**user_in_db.dict()).dict()
    access_token = create_user_access_token(settings.SECRET_KEY, settings.ALGORITHM, data=data_dict,
                                            expires_delta=expire_delta)

    token = Token(
        access_token=access_token,
        token_type=TOKEN_TYPE_BEARER
    )

    return token


@router.post("/login")
async def post_login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Authenticate for username and password and then generate and return token for the username
    :param form_data:
    :return:
    """
    user_in_db: UserInDB | bool = authenticate_user(get_fake_db(), form_data.username, form_data.password)
    if not isinstance(user_in_db, UserInDB):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    expire_delta = timedelta(minutes=15)
    data_dict: dict = User(**user_in_db.dict()).dict()
    access_token = create_user_access_token(settings.SECRET_KEY, settings.ALGORITHM, data=data_dict,
                                            expires_delta=expire_delta)

    response.set_cookie(
        "access_token",
        value=f"bearer {access_token}",
        # domain="http://localhost:9999",
        # httponly=True,
        # max_age=1800,
        # expires=1800,
    )

    token = Token(
        access_token=access_token,
        token_type=TOKEN_TYPE_BEARER
    )
    return token


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    return User(**current_user.dict())


@router.get("/me1")
async def read_users_me(current_user: User = Depends(get_current_user_from_api_key)):
    return current_user
