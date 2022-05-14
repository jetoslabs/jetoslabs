from fastapi import APIRouter
from fastapi.requests import Request

from common.aws.s3 import create_bucket, list_buckets, upload_file, download_file

router = APIRouter()

"""
Note: Using `Request` in route methods: a. to get logger contextualized by middlewares
"""

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
