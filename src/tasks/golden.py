from prefect import task
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from db.models import SilverRatesModel
from db.models.golden_rates import GoldenRatesModel
from db.session import get_async_session
from schemas.golden_rates import GoldenRatesSchema
from schemas.silver_rates import SilverRatesSchema


@task(name="get-silver-rates-task")
async def get_silver_rows(object_key: str) -> list[SilverRatesSchema]:
    session_factory = get_async_session()

    async with session_factory() as session:
        stmt = select(SilverRatesModel).where(SilverRatesModel.object_key == object_key)

        result = await session.execute(statement=stmt)

        return [
            SilverRatesSchema.model_validate(rate) for rate in result.scalars().all()
        ]


@task(name="transform-to-gold-task")
async def transform_to_gold(
    silver_rows: list[SilverRatesSchema],
) -> list[GoldenRatesSchema]:
    rates: list[GoldenRatesSchema] = []

    for row in silver_rows:
        for rate in row.payload["rates"]:
            rates.append(
                GoldenRatesSchema(
                    rate_date=row.rates_timestamp,
                    num_code=rate["num_code"],
                    char_code=rate["char_code"],
                    name=rate["name"],
                    rate=rate["rate"],
                )
            )

    return rates


@task(name="load-gold-task")
async def load_gold(
    rates: list[GoldenRatesSchema],
) -> None:
    if not rates:
        return

    session_factory = get_async_session()

    async with session_factory() as session:
        stmt = (
            insert(GoldenRatesModel)
            .values([rate.model_dump() for rate in rates])
            .on_conflict_do_nothing(
                constraint="uq_golden_rates_date_currency",
            )
        )

        await session.execute(stmt)
        await session.commit()
