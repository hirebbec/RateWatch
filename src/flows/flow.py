from prefect import flow

from core.config import settings
from flows.bronze import bronze_flow
from flows.golden import golden_flow
from flows.silver import silver_flow


@flow(name=settings().MAIN_FLOW_NAME)
async def main_flow():
    object_key = await bronze_flow()

    await silver_flow(object_key=object_key)
    await golden_flow(object_key=object_key)

    return object_key
