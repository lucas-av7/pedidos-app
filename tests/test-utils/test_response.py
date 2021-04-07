from api import utils


def test_if_has_response_method():
    assert hasattr(utils, "response")


def test_if_success_response_returns_expected_value_without_data():
    response = utils.response(msg="Store created successfully", code=200)
    expected = {
        "status": "Success",
        "status_code": 200,
        "message": "Store created successfully"
    }
    assert expected == response[0]
    assert 200 == response[1]


def test_if_success_response_returns_expected_value_with_data():
    data = {
        "id": 1,
        "name": "Lucas Vasconcelos",
        "email": "lucas@email.com",
        "phone": "(85) 90000-0000"
    }

    response = utils.response(msg="User created successfully", code=201, data=data)
    expected = {
        "status": "Success",
        "status_code": 201,
        "message": "User created successfully",
        "data": data
    }
    assert expected == response[0]
    assert 201 == response[1]


def test_if_error_response_returns_expected_value():
    response = utils.response(msg="Method not allowed", code=405)
    expected = {
        "status": "Error",
        "status_code": 405,
        "message": "Method not allowed"
    }
    assert expected == response[0]
    assert 405 == response[1]
