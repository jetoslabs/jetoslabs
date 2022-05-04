import random
import string
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from logger import get_child_logger


class TracerMiddleware(BaseHTTPMiddleware):

    def __init__(self, logger, app: ASGIApp):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request, call_next):
        trace = ''.join(random.choices(string.hexdigits, k=9))
        # Logger field name 'trace_id'
        child_logger = get_child_logger(self.logger, trace_id=trace)
        child_logger.bind(request_path=request.url.path).info("Start request")

        start_time = time.time()
        request.scope.update(logger=child_logger)  # passing child_logger with trace id in request
        response = await call_next(request)
        response_time_ms = round((time.time() - start_time) * 1000, 2)

        child_logger.bind(
            request_path=request.url.path, response_time_ms=response_time_ms, status_code=response.status_code
        ).info("Finish request")
        return response
