from prefect import flow

from tasks.silver import get_rates_from_s3, parse_rates_html, upload_to_db


@flow(name="silver-flow")
async def silver_flow(object_key: str) -> str:
    html = await get_rates_from_s3(full_key=object_key)

    payload = await parse_rates_html(html=html)

    await upload_to_db(
        source_object_key=object_key,
        payload=payload,
    )

    return object_key
