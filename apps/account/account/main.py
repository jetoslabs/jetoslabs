import uvicorn

from account.api.api_v1 import api
from account.core.description import description
from account.core.logger import logger
from account.core.server_resources import server_resources
from account.core.settings import settings
from common.config.config import load_config_folder
from common.fastapi_factory.fastapi_factory import FastAPIFactory
from logger import setup_logger


def create_app():
    # App specific settings
    settings.DESCRIPTION = description
    # Create FastAPI app
    app = FastAPIFactory.create_app(settings, logger)
    # Add application specific router
    app.include_router(router=api.router, prefix=f"/{settings.API_V1_STR}")
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    setup_logger()
    # Init all required server_resources fields
    # setup config
    server_resources.config = load_config_folder(settings.CONFIGURATION_LOC)
    # setup http_client
    server_resources.init_http_client()


@app.on_event("shutdown")
async def shutdown():
    await server_resources.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.APP_RELOAD,
        workers=settings.APP_WORKERS
    )
