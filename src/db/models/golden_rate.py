from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import CreatedAtMixin, IDMixin, UpdatedAtMixin


class GoldenRate(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "golden_rates"

    rate_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    num_code: Mapped[str] = mapped_column(String, nullable=False)
    char_code: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    rate: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "rate_date",
            "char_code",
            name="uq_golden_rates_date_currency",
        ),
    )
