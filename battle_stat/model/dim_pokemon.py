from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from battle_stat import Base


class PokemonDimension(Base):
    __tablename__ = 'dim_pokemon'

    id = Column(Integer, primary_key=True)
    poke_id = Column(Integer, unique=True)
    name = Column(String(100))
    speed = Column(Integer)
