import json


def error_response(msg, code):
    response = {
        "status": "Error",
        "status_code": code,
        "message": msg
    }
    return json.dumps(response), code
