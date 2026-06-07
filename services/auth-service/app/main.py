from fastapi import FastAPI
from app.api.router import api_router


app =  FastAPI(
    title="Auth Service"
)

app.include_router(api_router)

@app.get("/health")
async def helth_check():
    return{
        "Service": "Auth Service",
        "Status": "running "
    }
    