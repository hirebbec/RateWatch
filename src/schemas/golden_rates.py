from datetime import date
from decimal import Decimal

from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, UpdatedAtSchema


class CreateGoldenRatesSchema(BaseSchema):
    rate_date: date
    num_code: str
    char_code: str
    name: str
    rate: Decimal


class GetGoldenRatesSchema(CreateGoldenRatesSchema, CreatedAtSchema, UpdatedAtSchema): ...
