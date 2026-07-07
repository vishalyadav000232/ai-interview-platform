from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
import logging
import httpx

from app.core.config import settings
from app.services.build_forword_service import build_forward_headers
from app.core.exception import GatewayException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume", tags=["Resume Proxy"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def resume_proxy_request(
    path: str,
    request: Request
):
    target_url = f"{settings.RESUME_SERVICE_URL}/resume/{path}"

    request_id = getattr(request.state, "request_id", None)

    logger.info(
        "Incoming resume proxy request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": path,
            "target_url": target_url,
        }
    )

    body = await request.body()
    headers = build_forward_headers(request)

    client: httpx.AsyncClient | None = getattr(
        request.app.state,
        "http_client",
        None
    )

    if client is None:
        logger.error(
            "HTTP client is missing from app.state",
            extra={"request_id": request_id}
        )

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
            "Resume service response received",
            extra={
                "request_id": request_id,
                "status_code": upstream_response.status_code,
                "target_url": target_url,
            }
        )

    except httpx.RequestError as exc:
        logger.exception(
            "Resume service unavailable",
            extra={
                "request_id": request_id,
                "target_url": target_url,
                "method": request.method,
                "error": str(exc),
            }
        )

        raise GatewayException(
            message="Resume service unavailable",
            status_code=503
        )

    response = Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        media_type=upstream_response.headers.get("content-type")
    )

    excluded_headers = {
        "content-encoding",
        "transfer-encoding",
        "connection",
        "content-length",
    }

    for key, value in upstream_response.headers.items():
        if key.lower() not in excluded_headers:
            response.headers[key] = value

    return response