"""Controller/TCS errors retain their original response and gain descriptions."""

import pytest

from pf400 import DeviceError
from pf400.protocol import parse_response


def test_bare_no_attach_error_has_meaning_and_recovery_hint():
    with pytest.raises(DeviceError) as caught:
        parse_response("FreeMode 1", "-1009")
    error = caught.value
    assert error.code == -1009 and error.raw == "-1009"
    assert error.command == "FreeMode 1"
    assert "No robot attached" in str(error)
    assert "attach(1)" in error.hint
    assert "attach(0)" in error.hint
    assert error.description


@pytest.mark.parametrize("code", [-1006, -1012, -1017, -1021, -1028, -1046, -2800, -2815, -2850, -2855])
def test_known_numeric_errors_have_descriptions(code):
    error = DeviceError(code, str(code), "test")
    assert error.description and error.description in str(error)
    assert error.raw == str(code)


def test_controller_text_is_preserved_next_to_description():
    error = DeviceError(-1009, "-1009 manufacturer extra detail", "FreeMode 1")
    assert error.raw == "-1009 manufacturer extra detail"
    assert "manufacturer extra detail" in str(error)
    assert "No robot attached" in str(error)


def test_unknown_code_keeps_manufacturer_explanation():
    error = DeviceError(-99999, "-99999 manufacturer detail", "Nop")
    assert error.description == "manufacturer detail"
    assert error.raw == "-99999 manufacturer detail"


def test_unknown_bare_code_is_still_reported():
    error = DeviceError(-99999, "-99999", "Nop")
    assert error.code == -99999 and error.raw == "-99999"
    assert "알 수 없는" in error.description
