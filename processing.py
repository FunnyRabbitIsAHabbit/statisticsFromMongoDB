"""
Process JSON.

@Developer: Stan Ermokhin
@Version: 0.0.1
"""

import datetime
from typing import Any

import datamodel


class MainApp:

    @staticmethod
    def convert_request_json_to_valid_dict(json_data: str) -> dict[str, Any]:
        return datamodel.Request.model_validate_json(json_data).model_dump()

    @staticmethod
    def convert_response_json_to_valid_dict(json_data: str) -> dict[str, Any]:
        return datamodel.Response.model_validate_json(json_data).model_dump()

    @staticmethod
    def unpack_value(model_dict: dict[str, Any], value_tag: str) -> tuple[Any]:
        _res: Any = model_dict.get(value_tag)
        if "dt" in value_tag:
            _res: Any = DateTimeConverter.str_to_dt(_res)
        return _res


class DateTimeConverter:

    @staticmethod
    def dt_to_str(datetime_obj: datetime.datetime, cut_group: str) -> str:
        lesser_groups: list[datamodel.BiggerGroup] = [datamodel.BiggerGroup.hour,
                                                      datamodel.BiggerGroup.minute,
                                                      datamodel.BiggerGroup.second]

        if cut_group == datamodel.BiggerGroup.hour:
            lesser_groups.remove(datamodel.BiggerGroup.hour)
        elif cut_group == datamodel.BiggerGroup.month:
            lesser_groups.append(datamodel.BiggerGroup.day)

        kwargs: dict[datamodel.BiggerGroup, int] = {_argument: (0 if _argument != datamodel.BiggerGroup.day
                                                                else 1)
                                                    for _argument in lesser_groups}
        return datetime_obj.replace(**kwargs).isoformat(timespec="seconds")

    @staticmethod
    def str_to_dt(datetime_obj: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(datetime_obj)
