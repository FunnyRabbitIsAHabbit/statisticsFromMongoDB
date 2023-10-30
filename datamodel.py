"""
Datamodels.

@Developer: Stan Ermokhin
@Version: 0.0.1
"""

from enum import Enum

from pydantic import BaseModel, Field, ValidationError
from telegram.ext.filters import MessageFilter, Message

ACCEPTABLE_DATETIME_REGEX: str = r"/(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+)" \
                                 r"|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d)" \
                                 r"|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d)/"
DATE_FORMAT: str = "yyyy-MM-dd'T'HH:mm:ss"


class BiggerGroup(str, Enum):
    month: str = "month"
    day: str = "day"
    hour: str = "hour"
    minute: str = "minute"
    second: str = "second"


class Request(BaseModel):
    dt_from: str = Field(pattern=ACCEPTABLE_DATETIME_REGEX)
    dt_upto: str = Field(pattern=ACCEPTABLE_DATETIME_REGEX)
    group_type: str


class Response(BaseModel):
    dataset: list[int]
    labels: list[str]


class MessageFilterJSON(MessageFilter):

    def filter(self, message: Message) -> bool | dict[str, list] | None:

        try:
            Request.model_validate_json(json_data=message.text, strict=True)
            return True

        except ValidationError as validation_error:
            print(validation_error)
            return False
