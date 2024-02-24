from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from battle_stat import Base


class AttackFact(Base):
    __tablename__ = 'fact_attack'

    id = Column(Integer, primary_key=True)
    stat_changed = Column(Float)
    effort_ev = Column(Integer)
    stat_id = Column(Integer, ForeignKey('dim_stat.id'))
    move_id = Column(Integer, ForeignKey('dim_move.id'))
    iv = Column(Float)
    level = Column(Integer)
    nature_modifier = Column(Float)
    pokemon_id = Column(Integer, ForeignKey('dim_pokemon.id'))
    hp = Column(Integer)

    stat = relationship('StatDimension', foreign_keys=[stat_id])
    move = relationship('MoveDimension', foreign_keys=[move_id])
    pokemon = relationship('PokemonDimension', foreign_keys=[pokemon_id])
