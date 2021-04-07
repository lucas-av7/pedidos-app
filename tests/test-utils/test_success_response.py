from api.utils import responses


def test_if_has_success_response_method():
    assert hasattr(responses, "success_response")


def test_if_success_response_returns_expected_value_without_data():
    response = responses.success_response(msg="Store created successfully", code=200)
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

    response = responses.success_response(msg="User created successfully", code=201, data=data)
    expected = {
        "status": "Success",
        "status_code": 201,
        "message": "User created successfully",
        "data": data
    }
    assert expected == response[0]
    assert 201 == response[1]
