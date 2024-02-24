from sqlalchemy import Column, Integer, String

from battle_stat import Base


class MoveDimension(Base):
    __tablename__ = 'dim_move'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    power = Column(Integer)
