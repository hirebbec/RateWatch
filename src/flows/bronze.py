from prefect import flow

from tasks.bronze import fetch_rates, upload_rates_to_s3
from utils.build_key import build_bronze_rates_key


@flow(name="bronze-flow")
async def bronze_flow() -> str:
    data = await fetch_rates()

    object_key = build_bronze_rates_key()

    await upload_rates_to_s3(
        full_key=object_key,
        data=data,
        content_type="text/html; charset=utf-8",
    )

    return object_key
