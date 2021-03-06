import aiohttp
from fastapi import APIRouter, Depends
from fastapi.requests import Request

from concepts.api.deps import get_http_client
from concepts.controller import controller

router = APIRouter()

"""
Note: Using `Request` in route methods: a. to get logger contextualized by middlewares
"""


@router.get("/")
def hello(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/hello")
    return "hello"


@router.get("/ping_google")
async def ping_google(req: Request, http_client: aiohttp.ClientSession = Depends(get_http_client)):
    logger = req.scope.get("logger")
    logger.debug("/ping_google")
    res, body = await controller.ping_google(http_client, logger=logger)
    return body
