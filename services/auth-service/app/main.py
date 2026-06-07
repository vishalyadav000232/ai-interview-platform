from fastapi import FastAPI



app =  FastAPI(
    title="Auth Service"
)

@app.get("/health")
async def helth_check():
    return{
        "Service": "Auth Service",
        "Status": "running "
    }
    