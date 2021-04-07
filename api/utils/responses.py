import json


def error_response(msg, code):
    response = {
        "status": "Error",
        "status_code": code,
        "message": msg
    }
    return json.dumps(response), code


def success_response(msg, code, data=None):
    response = {
        "status": "Success",
        "status_code": code,
        "message": msg
    }

    if data:
        response["data"] = data

    return response, code
