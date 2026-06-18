import uuid
import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    
    
    async def dispatch(self, request: Request , call_next):
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        response = await call_next(request)
        
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        )
        
        response.headers["X-Request-ID"] = request_id

        return response
        
        