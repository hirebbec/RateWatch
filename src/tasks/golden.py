from prefect import task
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from db.models import SilverRatesModel
from db.models.golden_rates import GoldenRatesModel
from db.session import get_async_session


@task(name="get-silver-rates-task")
async def get_silver_rows(object_key: str) -> list[SilverRatesModel]:
    session_factory = get_async_session()

    async with session_factory() as session:
        result = await session.execute(
            select(SilverRatesModel).where(SilverRatesModel.object_key == object_key)
        )

        return list(result.scalars().all())


@task(name="transform-to-gold-task")
async def transform_to_gold(
    silver_rows: list[SilverRatesModel],
) -> list[dict]:
    result = []

    for row in silver_rows:
        for rate in row.payload["rates"]:
            result.append(
                {
                    "rate_date": row.rates_timestamp,
                    "num_code": rate["num_code"],
                    "char_code": rate["char_code"],
                    "name": rate["name"],
                    "rate": rate["rate"],
                }
            )

    return result


@task(name="load-gold-task")
async def load_gold(
    rows: list[dict],
) -> None:
    if not rows:
        return

    session_factory = get_async_session()

    async with session_factory() as session:
        stmt = (
            insert(GoldenRatesModel)
            .values(rows)
            .on_conflict_do_nothing(
                constraint="uq_golden_rates_date_currency",
            )
        )

        await session.execute(stmt)
        await session.commit()
