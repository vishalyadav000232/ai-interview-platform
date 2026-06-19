import logging

import httpx
from fastapi import APIRouter, HTTPException, Request, Response
from app.core.exception import GatewayException

from app.core.config import settings
from app.services.build_forword_service import build_forward_headers

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth Proxy"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def auth_proxy_request(path: str, request: Request):
    target_url = f"{settings.AUTH_SERVICE_URL}/auth/{path}"

    logger.info(
        "Incoming auth proxy request",
        extra={
            "method": request.method,
            "path": path,
            "target_url": target_url,
        }
    )

    body = await request.body()

    headers = build_forward_headers(request)

    headers.pop("host", None)

    client: httpx.AsyncClient | None = getattr(
        request.app.state,
        "http_client",
        None
    )

    if client is None:
        logger.error("HTTP client is missing from app.state")

        raise HTTPException(
            status_code=500,
            detail="Gateway HTTP client not initialized"
        )

    try:
        upstream_response = await client.request(
            method=request.method,
            url=target_url,
            content=body,
            headers=headers,
            params=request.query_params,
            cookies=request.cookies,
        )

        logger.info(
            "Auth service response received",
            extra={
                "status_code": upstream_response.status_code,
                "target_url": target_url,
            }
        )

    except httpx.TimeoutException as exc:
        logger.exception(
            "Auth service request timed out",
            extra={
                "target_url": target_url,
                "method": request.method,
            }
        )

        raise HTTPException(
            status_code=504,
            detail="Auth service timeout"
        ) from exc

    except httpx.RequestError as exc:
        logger.exception(
            "Auth service unavailable",
            extra={
                "target_url": target_url,
                "method": request.method,
                "error": str(exc),
            }
        )

        raise GatewayException(
            message="Auth service unavailable",
            status_code=503
        )

    response = Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        media_type=upstream_response.headers.get("content-type")
    )

    for key, value in upstream_response.headers.items():
        if key.lower() == "set-cookie":
            response.headers.append("set-cookie", value)

    return response