from datetime import timedelta

import logger
from common.users.hashing import verify_password
from common.users.schemas import UserInDB, User, TokenData
from common.users.user_exceptions import credential_exception
from common.auth.tokenizing import decode_access_token, create_access_token


fake_users_db = {
    "johndoe@example.com": {
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$MC3tRmHqMCP53ykYF0cy.Oge3dUXPAybs9g8K/8V5Y0sh6grepE..",
        "disabled": False,
    },
    "alice@example.com": {
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def get_user_in_db(db, email: str) -> None | UserInDB:
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str) -> bool | UserInDB:
    user = get_user_in_db(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user_access_token(data: dict, expires_delta: timedelta | None = None, *, sub: str = None) -> str:
    access_token: str = create_access_token(data, expires_delta, sub=sub)
    return access_token


def get_current_user_from_token(token: str) -> User:
    try:
        token_data_dict: dict = decode_access_token(token)
    except Exception as e:
        logger.get_logger().bind(e=e).error("Cannot decode access token")
        raise credential_exception

    token_data: TokenData = TokenData(**token_data_dict)
    if not token_data.email:
        raise credential_exception
    user = get_user_in_db(fake_users_db, token_data.email)
    if not user:
        raise credential_exception
    return user
