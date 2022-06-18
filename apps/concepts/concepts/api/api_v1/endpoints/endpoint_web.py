from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, RedirectResponse

from common.auth.constants import API_KEY, TOKEN_TYPE_BEARER
from common.auth.tokenizing import Token
from common.users.schemas import UserInDB, User
from common.users.user import authenticate_user, create_user_access_token
from concepts.api.deps import get_fake_db, get_current_user_from_api_key
from concepts.core.description import description
from concepts.core.resources import server_resources
from concepts.core.settings import settings
from concepts.templates import TEMPLATES
from concepts.templates.schema_home import PublicHomeSchema

router = APIRouter()


@router.get("/", tags=["web"])
async def get_home(request: Request) -> dict:
    home: PublicHomeSchema = PublicHomeSchema(
        title=settings.NAME,
        desc=description,
        config=server_resources.get_config()
    )
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "home": home},
    )


@router.get("/login", tags=["web"])
async def get_login(request: Request) -> dict:
    return TEMPLATES.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.post("/login", tags=["web"])
async def post_login(
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    user_in_db: UserInDB | bool = authenticate_user(get_fake_db(), form_data.username, form_data.password)
    if not isinstance(user_in_db, UserInDB):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    expire_delta = timedelta(minutes=15)
    data_dict: dict = User(**user_in_db.dict()).dict()
    access_token = create_user_access_token(settings.SECRET_KEY, settings.ALGORITHM, data=data_dict,
                                            expires_delta=expire_delta)

    response.set_cookie(
        API_KEY,
        value=f"bearer {access_token}",
        # domain=f"{settings.NAME}.{user_in_db.email}",
        # httponly=True,
        # max_age=1800,
        # expires=1800,
    )

    token = Token(
        access_token=access_token,
        token_type=TOKEN_TYPE_BEARER
    )
    return token.dict()
    # return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)

    # response = templates.TemplateResponse("auth/login.html", form.__dict__)

    # home: PublicHomeSchema = PublicHomeSchema(
    #     title=settings.NAME,
    #     desc=description,
    #     config=server_resources.get_config()
    # )
    # return TEMPLATES.TemplateResponse(
    #     "index.html",
    #     {"request": request, "home": home},
    # )


@router.get("/logout", tags=["web"])
async def get_logout(
        request: Request,
        response: Response,
        # current_user: User = Depends(get_current_user_from_api_key)
):
    response.delete_cookie(
        API_KEY,
    )
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

