from fastapi import APIRouter, Depends
from fastapi.requests import Request

from concepts.api.deps import get_current_active_admin_user
from concepts.core.resources import server_resources

router = APIRouter()


@router.get("/config", dependencies=[Depends(get_current_active_admin_user)])
def get_config(req: Request):
    logger = req.scope.get("logger")
    logger.debug("/config")
    return server_resources.get_config()
