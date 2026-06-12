from datetime import datetime, timedelta, timezone
from uuid import UUID , uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

class SecurityService:

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

    @classmethod
    def hash_password(cls,password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls,plain_password: str,hashed_password: str) -> bool:
        return cls.pwd_context.verify(
            plain_password,
            hashed_password
        )