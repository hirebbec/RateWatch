from datetime import date, timedelta
from typing import Sequence

from sqlalchemy import select, true

from db.models import GoldenRate
from db.repository.base import BaseDatabaseRepository
from schemas.golden_rates import GetGoldenRatesSchema


class RateRepository(BaseDatabaseRepository):
    async def get_rates(
        self, date_start: date | None = None, date_end: date | None = None
    ) -> Sequence[GetGoldenRatesSchema]:
        query = select(GoldenRate).filter(
            (GoldenRate.rate_date >= date_start) if date_start else true(),
            (GoldenRate.rate_date < date_end + timedelta(days=1)) if date_end else true(),
        )

        result = await self._session.execute(query)

        return [GetGoldenRatesSchema.model_validate(rate) for rate in result.scalars().all()]

    async def get_rates_by_char_code(
        self,
        char_code: str,
        date_start: date | None = None,
        date_end: date | None = None,
    ) -> Sequence[GetGoldenRatesSchema]:
        query = select(GoldenRate).filter(
            GoldenRate.char_code == char_code,
            (GoldenRate.rate_date >= date_start) if date_start else true(),
            (GoldenRate.rate_date < date_end + timedelta(days=1)) if date_end else true(),
        )

        result = await self._session.execute(query)

        return [GetGoldenRatesSchema.model_validate(rate) for rate in result.scalars().all()]
