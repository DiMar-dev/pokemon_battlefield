from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from battle_stat import Base


class StatDimension(Base):
    __tablename__ = 'dim_stat'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    change = Column(String(100))
    move_id = Column(Integer, ForeignKey('dim_move.id'))

    move = relationship('MoveDimension', foreign_keys=[move_id])
