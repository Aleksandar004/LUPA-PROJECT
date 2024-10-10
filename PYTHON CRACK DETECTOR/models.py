from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CrackDetails(Base):
    __tablename__ = 'CrackDetails'
    id = Column(Integer, primary_key=True)
    crack_name = Column(String)
    crack_length = Column(Float)
    coordinates_id = Column(Integer, ForeignKey('CrackCoordinates.id'))

    coordinates = relationship("CrackCoordinates", back_populates="details")

class CrackCoordinates(Base):
    __tablename__ = 'CrackCoordinates'
    id = Column(Integer, primary_key=True)
    x_start = Column(Integer)
    y_start = Column(Integer)
    x_end = Column(Integer)
    y_end = Column(Integer)

    details = relationship("CrackDetails", back_populates="coordinates")
