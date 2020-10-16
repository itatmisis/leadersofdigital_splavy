from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Yard(Base):
    __tablename__ = "yard"

    id = Column(Integer, primary_key=True, index=True)
    position_lat = Column(Float)
    position_lon = Column(Float)


class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, index=True)
    position_lat = Column(Float)
    position_lon = Column(Float)
    yard_id = Yard(Integer, ForeignKey("yard.id"))


class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    a_lat = Column(Float)
    a_lon = Column(Float)
    b_lat = Column(Float)
    b_lon = Column(Float)
    c_lat = Column(Float)
    c_lon = Column(Float)
    d_lat = Column(Float)
    d_lon = Column(Float)


class ParkingLot(Base):
    __tablename__ = "parking_lot"

    id = Column(Integer, primary_key=True, index=True)
    position_lat = Column(Float)
    position_lon = Column(Float)
    state = Column(String)
    yard_id = Yard(Integer, ForeignKey("yard.id"))
    points_id = Points(Integer, ForeignKey("points.id"))

