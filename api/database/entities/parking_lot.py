from typing import Optional

from pydantic.main import BaseModel

from database.entities.figure import Figure
from database.entities.geographical_figure import GeographicalFigure
from database.entities.geographical_point import GeographicalPoint
from database.entities.point import Point


class ParkingLot(BaseModel):
    id: float
    map_location: GeographicalPoint
    map_figure: GeographicalFigure
    photo_location: Point
    photo_figure: Optional[Figure]
