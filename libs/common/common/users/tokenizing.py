from datetime import timedelta, datetime

from jose import jwt, JWTError
from pydantic import BaseModel

from common.users.user import User, get_user_in_db, fake_users_db
from common.users.user_exceptions import credential_exception


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(User):
    expires_at: datetime

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    to_encode = data.copy()
    # add expires_at info
    if not timedelta:
        expires_at = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires_at = datetime.utcnow() + expires_delta
    expires_at_encodable = expires_at.isoformat() # jwt.encode throws exception for datetime.datetime instance type
    to_encode.update({"expires_at": expires_at_encodable})
    # encode claim set and return jwt string
    encoded_jwt: str = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    try:
        payload: dict = jwt.decode(token, SECRET_KEY, ALGORITHM)
        token_data: TokenData = TokenData(**payload)
        if not token_data:
            raise credential_exception
        return token_data
    except JWTError as e:
        raise credential_exception


def get_current_user_from_token(token: str) -> User:
    token_data: TokenData = decode_access_token(token)
    if not token_data.email:
        raise credential_exception
    user = get_user_in_db(fake_users_db, token_data.email)
    if not user:
        raise credential_exception
    return user
