from pydantic.main import BaseModel


class Quaternion(BaseModel):
    x: float
    y: float
    z: float
    w: float
