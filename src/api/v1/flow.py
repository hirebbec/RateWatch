from fastapi import APIRouter
from prefect.deployments import run_deployment

from core.config import settings

router = APIRouter(prefix="/flows", tags=["Flows"])


@router.post("/rates")
async def run_rates_flow():
    flow_run = await run_deployment(
        name=f"{settings().MAIN_FLOW_NAME}/{settings().MAIN_DEPLOYMENT_NAME}",
    )

    return {
        "flow_run_id": str(flow_run.id),
    }
