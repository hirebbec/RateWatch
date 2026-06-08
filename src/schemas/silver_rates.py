from datetime import date

from schemas.base import BaseSchema


class SilverRatesSchema(BaseSchema):
    object_key: str
    rates_timestamp: date
    payload: dict
