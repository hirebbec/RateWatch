import json

from prefect import flow

from tasks.bronze import fetch_rates, upload_rates_to_s3
from utils.build_key import build_bronze_rates_key


@flow(name="bronze-exchange-rates")
async def bronze_exchange_rates_flow(base_currency: str = "USD") -> str:
    payload = await fetch_rates(base_currency)

    object_key = build_bronze_rates_key(base_currency)

    data = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    await upload_rates_to_s3(
        full_key=object_key,
        data=data,
        content_type="application/json",
    )

    return object_key