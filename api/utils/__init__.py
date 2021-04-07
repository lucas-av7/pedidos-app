def response(msg, code, data=None):
    response = {
        "status": "Success" if code < 400 else "Error",
        "status_code": code,
        "message": msg
    }

    if data:
        response["data"] = data

    return response, code
