from datetime import date
from decimal import Decimal


from schemas.base import BaseSchema


class GoldenRatesSchema(BaseSchema):
    rate_date: date
    num_code: str
    char_code: str
    name: str
    rate: Decimal
