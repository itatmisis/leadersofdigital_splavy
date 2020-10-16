from typing import Optional
from fastapi import FastAPI

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/getAllIds")
async def read_body(user_token: str, lat: float, loc: float, radius: float = -1):
    return {"ok": True}


@app.get("/getYardInfo")
async def read_body(user_token: str, yard_id: int):
    return {"ok": True}
