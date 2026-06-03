import httpx
from prefect import task

from s3.client import s3_client_context


@task(retries=3, retry_delay_seconds=10)
async def fetch_rates(base_currency: str) -> dict:
    url = f"https://api.exchangerate.host/latest?base={base_currency}"

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()

    return response.json()

@task(retries=3, retry_delay_seconds=10)
async def upload_rates_to_s3(full_key: str, data: bytes, content_type: str | None = None):
    async with s3_client_context() as s3_storage:
        await s3_storage.upload_file(
            full_key=full_key,
            data=data,
            content_type=content_type,
        )