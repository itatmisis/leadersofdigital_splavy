from typing import List

from pydantic.main import BaseModel

from database.entities.camera import Camera
from database.entities.geographical_point import GeographicalPoint
from database.entities.parking_lot import ParkingLot


class Parking(BaseModel):
    id: int
    map_location: GeographicalPoint
    cameras: List[Camera]
    parking_lots: List[ParkingLot]
