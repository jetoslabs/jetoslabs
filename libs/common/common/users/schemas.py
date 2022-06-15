from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    email: str
    full_name: str | None = None
    disabled: bool | None = None
    is_admin: bool | None = None


class UserInDB(User):
    hashed_password: str


class TokenData(User):
    expires_at: datetime