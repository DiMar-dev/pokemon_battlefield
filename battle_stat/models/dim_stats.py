from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class StatDimension(Base):
    __tablename__ = 'dim_stat'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    change = Column(String)
    move_id = Column(Integer, ForeignKey('dim_move.id'))

    move = relationship('MoveDimension', foreign_keys=[move_id])
