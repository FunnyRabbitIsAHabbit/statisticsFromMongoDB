"""
Testing developed functionality.

@Developer: Stan Ermokhin
@Version: 0.0.1
"""

import json
from typing import Any

import database_control
import processing


class TestClass:
    with open("cases_for_tests.json") as json_file_io:
        CASES: list[dict] = json.load(json_file_io)

    DATABASE_APP: database_control.DatabaseControl = database_control.DatabaseControl()
    PROCESSING_APP: processing.MainApp = processing.MainApp()

    def generic_test(self, number: int) -> None:
        _input: str = self.CASES[number]["input"]
        _model_dict: dict[str, Any] = self.PROCESSING_APP.convert_request_json_to_valid_dict(_input)

        values: dict[str, Any] = {"dt_from": None, "dt_upto": None, "group_type": None}
        for key in _model_dict:
            values[key] = self.PROCESSING_APP.unpack_value(_model_dict, key)

        result: str = json.dumps(self.DATABASE_APP.get_result(**values))
        output: str = json.dumps(
            self.PROCESSING_APP.convert_response_json_to_valid_dict(
                self.CASES[number]["output"]
            )
        )

        assert result == output, f"Test {number + 1} NOT passed"

    def test_sample0(self) -> None:
        self.generic_test(0)

    def test_sample1(self) -> None:
        self.generic_test(1)

    def test_sample2(self) -> None:
        self.generic_test(2)
