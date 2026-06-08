import httpx
from prefect import task

from core.config import settings
from s3.storage import s3_storage_context


@task(retries=3, retry_delay_seconds=10, name="fetch-task")
async def fetch_rates() -> bytes:
    async with httpx.AsyncClient(
        timeout=settings().HTTP_TIMEOUT,
        follow_redirects=True,
        headers={
            "User-Agent": "RateWatch/0.1",
        },
    ) as client:
        response = await client.get(settings().CBR_URL)
        response.raise_for_status()

    return response.content


@task(retries=3, retry_delay_seconds=10, name="upload-s3-task")
async def upload_rates_to_s3(
    full_key: str,
    data: bytes,
    content_type: str | None = None,
) -> bool:
    async with s3_storage_context() as s3_storage:
        return await s3_storage.upload_file(
            full_key=full_key,
            data=data,
            content_type=content_type,
        )
