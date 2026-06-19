
from fastapi.requests import Request


def build_forward_headers(request: Request) -> dict:
    headers = dict(request.headers)

    headers.pop("host", None)
    headers.pop("content-length", None)

    request_id = getattr(request.state, "request_id", None)
    user_id = getattr(request.state, "user_id", None)
    user_role = getattr(request.state, "user_role", None)

    if request_id:
        headers["X-Request-ID"] = request_id

    if user_id:
        headers["X-User-ID"] = user_id

    if user_role:
        headers["X-User-Role"] = user_role

    return headers