from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from common.users.user import User, fake_users_db, UserInDB, fake_hash_password
from concepts.api.deps import oauth2_scheme, get_current_user

router = APIRouter()


# @router.get("/sample_login")
# async def sample_login(req: Request, token: str = Depends(oauth2_scheme)):
#     return {"token": token}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    user_in_db: UserInDB = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_in_db.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return {"access_token": user_in_db.email, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
