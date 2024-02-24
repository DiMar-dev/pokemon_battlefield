from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class MoveDimension(Base):
    __tablename__ = 'dim_move'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    power = Column(Integer)
