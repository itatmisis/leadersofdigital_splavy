from typing import Optional
from fastapi import FastAPI
from sql_app.db import Database

app = FastAPI()
db = Database('data/data.db')


@app.get("/getClosestIds")
async def read_body(user_token: str, lat: float, loc: float, radius: float = -1):
    return {"ok": True}


@app.get("/getYardInfo")
async def read_body(login: str, password_hash: str, yard_id: int):
    ok, error = db.check_user_ok(login, password_hash)
    if ok:
        ok, desc = db.api_yard_info(yard_id)
        return {"ok": False, "description": desc}
    else:
        return {"ok": False, "description": error}


@app.get("/login")
async def read_body(login: str, password_hash: str):
    ok, error = db.check_user_ok(login, password_hash)
    if ok:
        return {"ok": True}
    else:
        return {"ok": False, "description": error}

