from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from common.users.schemas import User, UserInDB
from common.users.tokenizing import Token, create_access_token
from common.users.user import authenticate_user
from concepts.api.deps import get_current_user, get_fake_db

router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Authenticate for username and password and then generate and return token for the username
    :param form_data:
    :return:
    """
    user_in_db: UserInDB | bool = authenticate_user(get_fake_db(), form_data.username, form_data.password)
    if not isinstance(user_in_db, UserInDB):
    # if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)

    expire_delta = timedelta(minutes=15)
    data_dict: dict= User(**user_in_db.dict()).dict()
    access_token = create_access_token(data=data_dict, expires_delta=expire_delta)

    token = Token(
        access_token=access_token,
        token_type="bearer"
    )

    return token


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return User(**current_user.dict())
