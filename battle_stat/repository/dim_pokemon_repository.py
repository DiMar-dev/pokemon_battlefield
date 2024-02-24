from battle_stat import db_session
from battle_stat.model.dim_pokemon import PokemonDimension


def get_all_dim_pokemons():
    return db_session.query(PokemonDimension).all()


def get_dim_pokemon_by_poke_id(poke_id):
    return db_session.query(PokemonDimension).filter(
        PokemonDimension.poke_id == poke_id).first()
