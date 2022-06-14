from pydantic import BaseModel

from common.users.hashing import verify_password

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


class User(BaseModel):
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user_in_db(db, email:str) -> None | UserInDB:
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
