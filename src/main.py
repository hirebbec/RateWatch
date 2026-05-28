import uvicorn
from fastapi import FastAPI

from api.router import api_router
from core.config import settings
from core.middlewares import middleware

app = FastAPI(
    title=settings().PROJECT_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
    middleware=middleware,
    swagger_ui_parameters={"operationsSorter": "method"},
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings().SERVER_HOST,
        port=settings().SERVER_PORT,
        workers=settings().SERVER_WORKERS_COUNT,
    )
