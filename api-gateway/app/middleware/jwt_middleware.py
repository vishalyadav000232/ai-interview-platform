from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from jose import jwt , JWTError

PUBLIC_PATHS = {
    "/health",
    "/auth/register",
    "/auth/login",
    "/auth/refresh",
    "/auth/forgot-password",
    "/auth/reset-password",
    "/auth/verify-email",
}





class JWTValidationMiddleware(BaseHTTPMiddleware):
    
    
    def __init__(self, app):
        super().__init__(app)
        
        
        self.public_path = {
    "/health",
    "/auth/register",
    "/auth/login",
    "/auth/refresh",
    "/auth/forgot-password",
    "/auth/reset-password",
    "/auth/verify-email",
}
    



    async def dispatch(self , request : Request , call_next):
        
        path = request.url.path 
        
        if path in  self.public_path or path.startswith("/docs") or path.startswith("/openapi"):
            return await call_next(request)
        
        
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Authorization token missing"
                }
            )
        
        token = auth_header.replace("Bearer ", "")
        
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            token_type = payload.get("type")
            user_id = payload.get("sub")
            # role = payload.get("role", "STUDENT") abhi role nahi set kar raha hu pauload me 

            if token_type != "access":
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Invalid token type"
                    }
                )

            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Invalid token payload"
                    }
                )

            request.state.user_id = user_id
            # request.state.user_role = role

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Invalid or expired token"
                }
            )

        return await call_next(request)
