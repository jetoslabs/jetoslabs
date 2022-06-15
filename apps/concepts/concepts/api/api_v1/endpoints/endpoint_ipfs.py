from fastapi import APIRouter, Depends

from common.ipfs_client.ipfs_client import ipfs_add_bytes, ipfs_cat
from common.users.schemas import User
from concepts.api.deps import get_ipfs_client, get_current_active_user

router = APIRouter()

@router.post("/ipfs_add")
async def post_ipfs_add(
        data: str,
        ipfs_client=Depends(get_ipfs_client),
        current_user: User = Depends(get_current_active_user),
):
    return ipfs_add_bytes(ipfs_client, data.encode('utf-8'))


@router.post("/ipfs_cat")
async def post_ipfs_cat(
        content_hash: str,
        ipfs_client=Depends(get_ipfs_client),
        current_user: User = Depends(get_current_active_user),
):
    return ipfs_cat(ipfs_client, content_hash)