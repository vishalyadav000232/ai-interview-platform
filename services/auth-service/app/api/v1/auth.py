from fastapi import APIRouter
from app.schemas.user import CreateUser


router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)




@router.get("/test")
async def test_route():
    return {
        "suceess" : True
    }
    
@router.post('/register')
def register(user : CreateUser):
    return  {
        "user" : user
    }