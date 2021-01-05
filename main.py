from fastapi import Depends, FastAPI

from v1.routers import users, auth

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}