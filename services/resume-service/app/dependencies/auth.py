from uuid import UUID
from fastapi import Header


def get_current_user_id( x_user_id: UUID = Header( ...,alias="X-User-ID")) -> UUID:
    return x_user_id