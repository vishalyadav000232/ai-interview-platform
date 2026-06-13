

class AppException(Exception):
    def __init__(self, message: str, status_code: int ,  error_code: str | None = None):
        self.message = message
        self.status_code = status_code
        self.error_code: str | None = None
        super().__init__(message)
        
        
        
class UserAlreadyExistException(AppException):
    def __init__(self):
        super().__init__(
            message="Email already registered",
            status_code=409,
            error_code="EMAIL_ALREADY_EXISTS"
            
        )


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            status_code=401,
            error_code="INVALID_CREDENTIALS"
        )

class UserNotFound(AppException):
    def  __init__(self):
        super().__init__(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND"
            )


class UserInactiveException(AppException):
    def __init__(self):
        super().__init__(
            message="User account is inactive",
            status_code=403,
            error_code="USER_INACTIVE"
        )