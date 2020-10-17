import logging
from typing import Dict, Tuple, List

from fastapi import Depends

import utils
from auth import auth
from database.database import Database
from database.entities.geographical_point import GeographicalPoint
from database.entities.parking import Parking
from database.entities.user import User


def setup_routers(app):
    auth.setup_routers(app)

    @app.get("/closest/parking")
    async def read_body(lat: float, lon: float, radius: float = -1,
                        user: User = Depends(auth.fastapi_users.get_current_active_user)):
        try:
            center_location = GeographicalPoint(latitude=lat, longitude=lon)
            parkings: List[Parking] = await Database.find("parking", {})
            objects: Dict[int, GeographicalPoint] = dict()
            for parking in parkings:
                objects[parking.id] = GeographicalPoint(latitude=parking.map_location.latitude,
                                                        longitude=parking.map_location.longitude)

            inradius_parkings = utils.get_radius_objects(center_location, radius, objects)

            response_parkigns = [parking for parking in filter(lambda x: x.id in list(inradius_parkings.keys()),
                                                               parkings)]
            return {"ok": True, "data": response_parkigns}
        except Exception as e:
            logging.debug(e)
            return {"ok": False}

    @app.get("/closest/parking-lot")
    async def read_body(lat: float, lon: float, radius: float = -1,
                        user: User = Depends(auth.fastapi_users.get_current_active_user)):
        try:
            center_location = GeographicalPoint(latitude=lat, longitude=lon)
            parkings: List[Parking] = await Database.find("parking", {})
            objects: Dict[Tuple[int, int], GeographicalPoint] = dict()
            for parking in parkings:
                for parking_lot in parking.parking_lots:
                    objects[(parking.id, parking_lot.id)] = GeographicalPoint(
                        latitude=parking_lot.map_location.latitude,
                        longitude=parking_lot.map_location.longitude)

            inradius_parking_lots = utils.get_radius_objects(center_location, radius, objects)

            response_parking_lots = []
            for parking in parkings:
                response_parking_lots.extend([parking_lot for parking_lot in
                                              filter(lambda x: (parking.id, x.id) in list(inradius_parking_lots.keys()),
                                                     parking.parking_lots)])

            return {"ok": True, "data": response_parking_lots}
        except Exception as e:
            logging.debug(e)
            return {"ok": False}

    @app.get("/parking")
    async def read_body(parking_id: int, user: User = Depends(auth.fastapi_users.get_current_active_user)):
        return {"ok": True,
                "data": await Database.find_one("parking", {"id": parking_id})}

    @app.post("/report")
    async def read_body(parking_id: int, text: str, photo: str = None,
                        user: User = Depends(auth.fastapi_users.get_current_active_user)):
        return {"ok": True}
