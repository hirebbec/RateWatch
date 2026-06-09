from typing import Sequence

from fastapi import APIRouter, Body, Depends, status

from schemas.filters import DateFilterSchema
from schemas.golden_rates import GetGoldenRatesSchema
from services.rate import RateService

router = APIRouter(prefix="/rates", tags=["Rates"])


@router.post("", status_code=status.HTTP_200_OK, response_model=Sequence[GetGoldenRatesSchema])
async def get_rates(
    date_filter: DateFilterSchema = Body(), rate_service: RateService = Depends()
) -> Sequence[GetGoldenRatesSchema]:
    return await rate_service.get_rates(date_filter=date_filter)


@router.post("/{char_code}", status_code=status.HTTP_200_OK, response_model=Sequence[GetGoldenRatesSchema])
async def get_rates_char_code(
    char_code: str, date_filter: DateFilterSchema = Body(), rate_service: RateService = Depends()
) -> Sequence[GetGoldenRatesSchema]:
    return await rate_service.get_rates_by_char_code(char_code=char_code, date_filter=date_filter)
