from fastapi import APIRouter

from concepts.api.api_v1.endpoints import endpoint_hello, endpoint_eth, endpoint_s3

router = APIRouter()

router.include_router(router=endpoint_hello.router, prefix="/hello", tags=["hello"])
router.include_router(router=endpoint_eth.router, prefix="/eth", tags=["eth"])
router.include_router(router=endpoint_s3.router, prefix="/s3", tags=["s3"])
