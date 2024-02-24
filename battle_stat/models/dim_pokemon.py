from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class PokemonDimension(Base):
    __tablename__ = 'dim_pokemon'

    id = Column(Integer, primary_key=True)
    poke_id = Column(Integer, unique=True)
    name = Column(String)
    hp = Column(Integer)
    speed = Column(Integer)
