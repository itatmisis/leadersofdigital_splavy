from typing import Optional

from pydantic.main import BaseModel


class GeographicalPoint(BaseModel):
    latitude: float
    longitude: float
    altitude: Optional[float]
