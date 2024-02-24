from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


class BattleFact(Base):
    __tablename__ = 'fact_battle'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    pokemon_id_1 = Column(Integer, ForeignKey('dim_pokemon.id'))
    pokemon_id_2 = Column(Integer, ForeignKey('dim_pokemon.id'))
    attack_id_1 = Column(Integer, ForeignKey('fact_attack.id'))
    attack_id_2 = Column(Integer, ForeignKey('fact_attack.id'))
    battle_duration = Column(Integer) 
    winner_pokemon_id = Column(Integer, ForeignKey('dim_pokemon.id'))

    # Relationships (optional, for easier querying)
    pokemon_1 = relationship("PokemonDimension", foreign_keys=[pokemon_id_1])
    pokemon_2 = relationship("PokemonDimension", foreign_keys=[pokemon_id_2])
    attack_1 = relationship("AttackFact", foreign_keys=[attack_id_1])
    attack_2 = relationship("AttackFact", foreign_keys=[attack_id_2])
    winner = relationship("PokemonDimension", foreign_keys=[winner_pokemon_id])
