import time

from loguru import logger
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

middleware = []


if settings().USE_CORS_MIDDLEWARE:
    middleware.append(
        Middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=settings().CORS_ALLOW_ORIGIN_LIST,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    )

if settings().USE_TIMER_MIDDLEWARE:

    class TimerMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time

            message = (
                f"{request.method} {request.url.path} - {1000 * process_time:.4f} ms"
            )
            logger.debug(message)

            return response

    middleware.append(Middleware(TimerMiddleware))
