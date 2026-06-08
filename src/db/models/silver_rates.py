from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import IDMixin, CreatedAtMixin, UpdatedAtMixin


class SilverRatesModel(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "silver_rates"

    object_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    rates_timestamp: Mapped[date] = mapped_column(Date, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
