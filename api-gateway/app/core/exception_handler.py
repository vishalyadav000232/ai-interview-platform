import logging
from fastapi import Request 
from app.core.exception import GatewayException

from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)



async def gateway_exception_handler(
    request  : Request,
    exc : GatewayException
    
):
    logger.error(
        "Gateway exception",
        extra={
            "path": request.url.path,
            "message": exc.message
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )