from api.utils import responses
import json


def test_if_has_error_response_method():
    assert hasattr(responses, "error_response")


def test_if_error_response_returns_expected_value():
    response = responses.error_response(msg="Method not allowed", code=405)
    expected = {
        "status": "Error",
        "status_code": 405,
        "message": "Method not allowed"
    }
    assert json.dumps(expected) == response[0]
    assert 405 == response[1]
