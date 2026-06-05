import json
from typing import Any

from prefect import task

from s3.storage import s3_storage_context


@task(retries=3, retry_delay_seconds=10, name="get-from-s3-task")
async def get_rates_from_s3(full_key: str) -> bytes:
    async with s3_storage_context() as s3_storage:
        return await s3_storage.get_file(full_key=full_key)

@task(retries=3, retry_delay_seconds=10, name="parse-cbr-html-task")
async def parse_rates_html(html: bytes) -> dict[str, Any]:
    return parse_cbr_daily_html(html)


@task(retries=3, retry_delay_seconds=10, name="upload-to-db-task")
async def upload_to_db(
    source_object_key: str,
    payload: dict[str, Any],
) -> str:
    async with db_session_context() as session:
        await session.execute(
            text(
                """
                INSERT INTO currency_rates_silver (
                    source,
                    dataset,
                    source_object_key,
                    rates_date,
                    payload
                )
                VALUES (
                    :source,
                    :dataset,
                    :source_object_key,
                    :rates_date,
                    CAST(:payload AS jsonb)
                )
                ON CONFLICT (source_object_key)
                DO UPDATE SET
                    rates_date = EXCLUDED.rates_date,
                    payload = EXCLUDED.payload
                """
            ),
            {
                "source": payload["source"],
                "dataset": payload["dataset"],
                "source_object_key": source_object_key,
                "rates_date": payload["date"],
                "payload": json.dumps(payload, ensure_ascii=False),
            },
        )

        await session.commit()

    return source_object_key

