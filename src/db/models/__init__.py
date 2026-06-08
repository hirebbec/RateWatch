__all__ = (
    "BaseModel",
    "SilverRatesModel",
    "GoldenRatesModel",
)

from db.models.base import BaseModel
from db.models.golden_rates import GoldenRatesModel
from db.models.silver_rates import SilverRatesModel
