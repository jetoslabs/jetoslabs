from pathlib import Path

import uvicorn
from fastapi import Security
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from concepts.api.api_v1 import api
from concepts.api.deps import get_current_active_admin_user_from_api_key
from concepts.core.description import description
from concepts.core.logger import logger
from concepts.core.resources import server_resources
from concepts.core.settings import settings
from common.fastapi_factory.fastapi_factory import FastAPIFactory
from logger import setup_logger


def create_app():
    # App specific settings
    settings.DESCRIPTION = description
    settings.NAME = "Concepts"
    # Create FastAPI app
    app = FastAPIFactory.create_app(settings, logger)
    # Add application specific router
    app.include_router(router=api.router, prefix=f"/{settings.API_V1_STR}")
    app.include_router(router=api.web_router)
    server_resources._api_routes = api.router.routes
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    # Begin with setup logger
    setup_logger()
    # Init all required server_resources fields
    base_path = Path(__file__).resolve().parent
    server_resources.setup_server_resources(base_path, settings)


@app.on_event("shutdown")
async def shutdown():
    await server_resources.close()


@app.get("/openapi.json", tags=["docs"])
async def get_open_api_endpoint(user=Security(get_current_active_admin_user_from_api_key)):
    response = JSONResponse(
        get_openapi(
            title=settings.NAME,
            version=settings.VERSION,
            description=description,
            contact={
                "name": settings.CONTACT_NAME,
                "url": settings.CONTACT_URL,
                "email": settings.CONTACT_EMAIL,
            },
            routes=app.routes)
    )
    return response


@app.get("/docs", tags=["docs"])
async def get_documentation(user=Security(get_current_active_admin_user_from_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.APP_RELOAD,
        workers=settings.APP_WORKERS
    )
