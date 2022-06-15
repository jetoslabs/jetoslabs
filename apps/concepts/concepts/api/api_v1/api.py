from fastapi import APIRouter

from concepts.api.api_v1.endpoints import endpoint_hello, endpoint_eth, endpoint_s3, endpoint_user, endpoint_admin, endpoint_ipfs

router = APIRouter()

router.include_router(router=endpoint_hello.router, prefix="/hello", tags=["hello"])
router.include_router(router=endpoint_user.router, prefix="/user", tags=["user"])
router.include_router(router=endpoint_admin.router, prefix="/admin", tags=["admin"])
router.include_router(router=endpoint_eth.router, prefix="/eth", tags=["eth"])
router.include_router(router=endpoint_ipfs.router, prefix="/ipfs", tags=["ipfs"])
router.include_router(router=endpoint_s3.router, prefix="/s3", tags=["s3"])
