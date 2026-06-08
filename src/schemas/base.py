from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, ValidationError
from typing_extensions import Self

from core.config import settings
from core.exceptions import ModelEncodeValidationError


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.astimezone(tz=settings().TIME_ZONE),
        },
    )

    @classmethod
    def model_encode(cls, *objs: Any) -> Self:
        try:
            return cls.model_validate(
                {
                    key: value
                    for obj in objs
                    for key, value in (jsonable_encoder(obj).items() if obj else [])
                }
            )
        except ValidationError:
            raise ModelEncodeValidationError("Validation error in model_encode")
