from fastapi import APIRouter
from fastapi.requests import Request

from concepts.controller import controller
from concepts.core.server_resources import server_resources

router = APIRouter()

"""
Note: Using `Request` in route methods: a. to get logger contextualized by middlewares
"""


@router.get("/")
def hello(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/hello")
    return "hello"


@router.get("/config")
def get_config(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/config")
    return server_resources.config


@router.get("/ping_google")
async def ping_google(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/ping_google")
    res, body = await controller.ping_google(logger=logger)
    return body

