

import logging 
from app.core.exceptions import AppException 
from fastapi import FastAPI  , Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def app_exception_handler(
    request : Request,
    exc : AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success":False,
            "message":exc.message,
            "error_code": exc.error_code
        }
    )
    
    
async def global_exception_handler(
    request : Request,
    exc : Exception
):
    logger.exception(
        "Unexpected server error"
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)