from datetime import timedelta, datetime

from jose import jwt, JWTError
from loguru import logger

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None, *, sub: str = None) -> str:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    # taking a copy of data
    to_encode = data.copy()
    # the JWT specification says that there's a key sub, with the subject of the token.
    # important thing to have in mind is that the sub key should have a unique identifier across the entire application, and it should be a string.
    if sub: to_encode.update({"sub": sub})
    # adding expires_at field in to_encode
    if not timedelta:
        expires_at = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires_at = datetime.utcnow() + expires_delta
    expires_at_encodable = expires_at.isoformat()  # jwt.encode throws exception for datetime.datetime instance type
    to_encode.update({"expires_at": expires_at_encodable})
    # encode claim set and return jwt string
    encoded_jwt: str = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError as e:
        logger.bind(e=e).error("Cannot decode access token")
        raise e
