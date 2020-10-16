from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getAllIds")
async def read_token(user_token: str, x: float, y: float, radius: float = -1):
    return user_token

