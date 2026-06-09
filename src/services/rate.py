from typing import Sequence

from fastapi import Depends

from db.repository.rate import RateRepository
from schemas.filters import DateFilterSchema
from schemas.golden_rates import GetGoldenRatesSchema
from services.base import BaseService


class RateService(BaseService):
    def __init__(self, rate_repository: RateRepository = Depends()) -> None:
        self._rate_repository = rate_repository

    async def get_rates(self, date_filter: DateFilterSchema) -> Sequence[GetGoldenRatesSchema]:
        return await self._rate_repository.get_rates(date_start=date_filter.date_start, date_end=date_filter.date_end)

    async def get_rates_by_char_code(
        self, char_code: str, date_filter: DateFilterSchema
    ) -> Sequence[GetGoldenRatesSchema]:
        return await self._rate_repository.get_rates_by_char_code(
            char_code=char_code,
            date_start=date_filter.date_start,
            date_end=date_filter.date_end,
        )
