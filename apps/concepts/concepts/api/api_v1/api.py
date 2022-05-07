from fastapi import APIRouter

from concepts.api.api_v1.endpoints import hello

router = APIRouter()

router.include_router(router=hello.router, prefix="/hello", tags=["hello"])
