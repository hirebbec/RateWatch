from datetime import date
from typing import Any

from sqlalchemy import Date, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import CreatedAtMixin, IDMixin, UpdatedAtMixin


class SilverRates(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "silver_rates"

    object_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    rates_timestamp: Mapped[date] = mapped_column(Date, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
