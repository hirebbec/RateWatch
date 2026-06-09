from datetime import date, datetime
from typing import Any

from bs4 import BeautifulSoup
from prefect import task
from sqlalchemy.dialects.postgresql import insert

from db.models import SilverRates
from db.session import get_async_session
from s3.storage import s3_storage_context


@task(retries=3, retry_delay_seconds=10, name="get-from-s3-task")
async def get_rates_from_s3(full_key: str) -> bytes:
    async with s3_storage_context() as s3_storage:
        return await s3_storage.get_file(full_key=full_key)


@task(
    retries=3,
    retry_delay_seconds=10,
    name="parse-cbr-html-task",
)
async def parse_rates_html(html: bytes) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    date_button = soup.select_one(".datepicker-filter_button")

    if date_button is None:
        raise ValueError("Rates date not found")

    rates_date = datetime.strptime(
        date_button.text.strip(),
        "%d.%m.%Y",
    ).date()

    table = soup.select_one("table.data")

    if table is None:
        raise ValueError("Rates table not found")

    rows = table.select("tr")[1:]

    rates = []

    for row in rows:
        cells = [td.get_text(strip=True) for td in row.select("td")]

        if len(cells) != 5:
            continue

        num_code, char_code, nominal, currency_name, rate = cells

        rates.append(
            {
                "num_code": num_code,
                "char_code": char_code,
                "nominal": int(nominal),
                "name": currency_name,
                "rate": float(rate.replace(",", ".")),
            }
        )

    return {
        "source": "cbr",
        "rates_date": rates_date.isoformat(),
        "rates": rates,
    }


@task(
    retries=3,
    retry_delay_seconds=10,
    name="upload-to-db-task",
)
async def upload_to_db(
    source_object_key: str,
    payload: dict[str, Any],
) -> None:
    session_factory = get_async_session()

    async with session_factory() as session:
        stmt = (
            insert(SilverRates)
            .values(
                object_key=source_object_key,
                rates_timestamp=date.fromisoformat(payload["rates_date"]),
                payload=payload,
            )
            .on_conflict_do_nothing(index_elements=["object_key"])
        )

        await session.execute(stmt)
        await session.commit()
