import loguru
from fastapi import FastAPI

from common.middleware import middleware_tracer
from common.settings.settings import Settings


class FastAPIFactory:
    @staticmethod
    def create_app(settings: Settings, logger: loguru.logger):
        app = FastAPI(
            # title=settings.NAME,
            # description=settings.DESCRIPTION,
            # version=settings.VERSION,
            # contact={
            #     "name": settings.CONTACT_NAME,
            #     "url": settings.CONTACT_URL,
            #     "email": settings.CONTACT_EMAIL,
            # },
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
        )

        # Add common Middleware routers
        app.add_middleware(middleware_tracer.TracerMiddleware, logger=logger)

        return app
