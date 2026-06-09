from datetime import date

from schemas.base import BaseSchema


class DateFilterSchema(BaseSchema):
    date_start: date | None = None
    date_end: date | None = None
