from fastapi import APIRouter

from api.healthcheck import router as healthcheck_router
from api.v1.rate import router as rate_router
from api.v1.flow import router as flow_router
from core.config import settings

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(rate_router)
v1_router.include_router(flow_router)

project_router = APIRouter(prefix=f"/{settings().PROJECT_NAME}")
project_router.include_router(v1_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(project_router)
api_router.include_router(healthcheck_router)
