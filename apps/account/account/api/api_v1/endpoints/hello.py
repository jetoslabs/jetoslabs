from fastapi import APIRouter
from fastapi.requests import Request

from account.controller import controller
from account.core.server_resources import server_resources
from account.schemas.schemas_account import NewAccountReq, NewAccountRes, GenAccountRes, GenAccountReq
from common.aws.s3 import create_bucket, list_buckets, upload_file, download_file

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


@router.post("/new_account", response_model=NewAccountRes)
async def new_account(req: Request, req_body: NewAccountReq) -> NewAccountRes:
    logger = req.scope.get("logger")
    logger.debug("/new_account")
    account, mnemonic = await controller.create_with_mnemonic(req_body.passphrase)
    res = NewAccountRes(
        address=account.address,
        key=account.key.hex(),
        privateKey=account.privateKey.hex(),
        mnemonic=mnemonic
    )
    return res


@router.post("/gen_account", response_model=GenAccountRes)
async def gen_account(req: Request, req_body: GenAccountReq) -> GenAccountRes:
    logger = req.scope.get("logger")
    logger.debug("/gen_account")
    account = await controller.gen_from_mnemonic(req_body.mnemonic, req_body.passphrase)
    res = GenAccountRes(
        address=account.address,
        key=account.key.hex(),
        privateKey=account.privateKey.hex(),
        mnemonic=req_body.mnemonic
    )
    return res


@router.get("/ping_google")
async def ping_google(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/ping_google")
    res, body = await controller.ping_google(logger=logger)
    return body


@router.get("/s3/bucket/create")
async def create_s3_bucket(req: Request):
    logger = req.scope.get("logger")
    s3_res = create_bucket(
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="",
        bucket_name="",
        logger=logger
    )
    return s3_res


@router.get("/s3/bucket/list")
async def list_s3_bucket(req: Request):
    logger = req.scope.get("logger")
    s3_res = list_buckets(
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="",
        logger=logger
    )
    return s3_res


@router.get("/s3/file/upload")
async def upload_s3_file(req: Request):
    logger = req.scope.get("logger")
    s3_res = upload_file(
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="",
        file_name="",
        bucket="",
        logger=logger
    )
    return s3_res


@router.get("/s3/file/download")
async def download_s3_file(req: Request):
    logger = req.scope.get("logger")
    s3_res = download_file(
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="",
        bucket="",
        object_name="",
        file_name="",
        logger=logger
    )
    return s3_res
