from typing import List

from pydantic.main import BaseModel

from database.entities.point import Point


class Figure(BaseModel):
    points: List[Point]
