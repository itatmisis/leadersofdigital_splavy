from fastapi import Depends

from auth import auth
from database.database import Database
from database.entities.user import User


def setup_routers(app):
    auth.setup_routers(app)

    @app.get("/closest/parking")
    async def read_body(lat: float, loc: float,
                        user: User = Depends(auth.fastapi_users.get_current_active_user), radius: float = -1):
        return {"ok": True}

    @app.get("/closest/parking-lot")
    async def read_body(lat: float, loc: float,
                        user: User = Depends(auth.fastapi_users.get_current_active_user), radius: float = -1):
        return {"ok": True}

    @app.get("/parking")
    async def read_body(parking_id: int, user: User = Depends(auth.fastapi_users.get_current_active_user)):
        return {"ok": True,
                "description":
                    Database.find_one("parking", {"_id": parking_id})}

    @app.post("/report")
    async def read_body(parking_id: int, user: User = Depends(auth.fastapi_users.get_current_active_user)):
        return {"ok": True}
