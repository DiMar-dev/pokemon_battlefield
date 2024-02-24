from battle_stat import DBCache
from battle_stat.database import save_list_data
from battle_stat.model.dim_move import MoveDimension
from battle_stat.model.dim_pokemon import PokemonDimension
from battle_stat.model.dim_stats import StatDimension
from battle_stat.model.fact_attack import AttackFact
from battle_stat.model.fact_battle import BattleFact
from battle_stat.repository.dim_move_repository import get_all_dim_moves, \
    get_dim_move_by_name
from battle_stat.repository.dim_pokemon_repository import get_all_dim_pokemons, \
    get_dim_pokemon_by_poke_id
from battle_stat.repository.dim_stats_repository import get_all_dim_stats, \
    get_dim_stat_by_type_name
from model.pokemon import Pokemon


def init_db_cache():
    """
        Initializes the database cache by loading and caching dimensions for moves, Pokémon, and stats.
        Populates global cache variables with data fetched from the database to optimize future data retrieval.
        """
    DBCache.DIM_MOVE_CACHE = {x.name for x in get_all_dim_moves()}
    DBCache.DIM_POKEMON_CACHE = {x.poke_id for x in get_all_dim_pokemons()}
    DBCache.DIM_STATS_CACHE = {(x.name, x.move.name) for x in
                               get_all_dim_stats()}


def take_battle_notes(attacker: Pokemon, defender: Pokemon,
                      battle_duration: float = None):
    """
        Records notes about a Pokémon battle, including details about the attacker, defender, and the battle outcome.
        Prepares and saves battle and attack facts to the database for later analysis.

        Args:
            attacker (Pokemon): The attacking Pokémon in the battle.
            defender (Pokemon): The defending Pokémon in the battle.
            battle_duration (float, optional): The duration of the battle in seconds. Defaults to None.

        This function creates and saves dimensional and factual data related to the battle and the Pokémon involved.
        """
    save_list = []
    attacker_tuple = __write_notes(attacker, save_list)
    defender_tuple = __write_notes(defender, save_list)

    winner = None
    if battle_duration:
        if attacker.hp > 0:
            winner = attacker_tuple[0]
        else:
            winner = defender_tuple[0]

    fact_battle = BattleFact(pokemon_1=attacker_tuple[0],
                             pokemon_2=defender_tuple[0],
                             attack_1=attacker_tuple[1],
                             attack_2=defender_tuple[1],
                             battle_duration_s=battle_duration,
                             winner=winner
                             )
    save_list.append(fact_battle)
    save_list_data(save_list)


def __write_notes(pokemon: Pokemon, save_list: list):
    """
        Records notes for a single Pokémon's performance in a battle, including its moves and stats.
        Updates the cache with new dimensional data and appends factual data to the save list for database storage.

        Args:
            pokemon (Pokemon): The Pokémon for which to write notes.
            save_list (list): A list to which new data records are appended for batch saving.

        Returns:
            tuple: A tuple containing the Pokémon's dimensional data and its latest attack fact.

        This function is intended to be used internally by `take_battle_notes` to process each Pokémon involved in a battle.
        """
    move = pokemon.current_attack.move
    attack = pokemon.current_attack

    if move.name not in DBCache.DIM_MOVE_CACHE:
        DBCache.DIM_MOVE_CACHE.add(move.name)
        dim_move = MoveDimension(name=move.name,
                                 power=move.power)
        save_list.append(dim_move)
    else:
        dim_move = get_dim_move_by_name(move.name)

    if pokemon.poke_id not in DBCache.DIM_POKEMON_CACHE:
        DBCache.DIM_POKEMON_CACHE.add(pokemon.poke_id)
        dim_pokemon = PokemonDimension(poke_id=pokemon.poke_id,
                                       name=pokemon.name,
                                       speed=pokemon.speed)
        save_list.append(dim_pokemon)
    else:
        dim_pokemon = get_dim_pokemon_by_poke_id(pokemon.poke_id)

    if (attack.stat_type, move.name) not in DBCache.DIM_STATS_CACHE:
        DBCache.DIM_STATS_CACHE.add((attack.stat_type, move.name))
        dim_stat = StatDimension(name=attack.stat_type,
                                 change=move.change,
                                 move=dim_move)
        save_list.append(dim_stat)
    else:
        dim_stat = get_dim_stat_by_type_name(attack.stat_type, move.name)

    fact_attack = AttackFact(stat_changed=attack.stat_changed,
                             effort_ev=attack.effort_ev,
                             stat=dim_stat,
                             move=dim_move,
                             iv=attack.iv,
                             level=attack.level,
                             nature_modifier=attack.nature_modifier,
                             pokemon=dim_pokemon,
                             hp=pokemon.hp)
    save_list.append(fact_attack)
    return dim_pokemon, fact_attack
