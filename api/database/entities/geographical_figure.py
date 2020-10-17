from typing import List

from pydantic.main import BaseModel

from database.entities.geographical_point import GeographicalPoint


class GeographicalFigure(BaseModel):
    points: List[GeographicalPoint]
