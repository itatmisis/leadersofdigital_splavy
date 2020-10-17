from typing import Optional

from pydantic.main import BaseModel

from database.entities.geographical_point import GeographicalPoint
from database.entities.quaternion import Quaternion


class Camera(BaseModel):
    id: int
    map_location: Optional[GeographicalPoint]
    rotation: Optional[Quaternion]
