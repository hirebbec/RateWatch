__all__ = (
    "BaseModel",
    "SilverRates",
    "GoldenRate",
)

from db.models.base import BaseModel
from db.models.golden_rate import GoldenRate
from db.models.silver_rate import SilverRates
