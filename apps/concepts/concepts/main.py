import uvicorn

from common.web3.web3_provider import get_w3_provider
from concepts.api.api_v1 import api
from concepts.core.config import setup_config
from concepts.core.description import description
from concepts.core.logger import logger
from concepts.core.server_resources import server_resources
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
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    # Begin with setup logger
    setup_logger()
    # Init all required server_resources fields
    # First setup config
    server_resources.config = setup_config()
    # setup http_client
    server_resources.init_http_client()
    # setup web3 provider
    server_resources.web3_provider = get_w3_provider(server_resources.config.SYSTEM.web3.provider_uri)


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
