import asyncio
from fastapi import FastAPI
import uvicorn
from database.database import engine, Base
from api.routes import router

app = FastAPI()
app.include_router(router)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
