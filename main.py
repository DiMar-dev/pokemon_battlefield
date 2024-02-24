import asyncio
from time import perf_counter

from battle_stat.battle_notes import init_db_cache, take_battle_notes
from fetch_poke_data import fetch_stats, fetch_data_sync, \
    POKE_API_POKEMON
from model.pokemon import Pokemon\


def fetch_init_data():
    """
        Initializes the application by loading and fetching Pokémon stats asynchronously.
        Measures and prints the time taken to fetch all Pokémon stats.
        """
    print('Loading pokemon data...')
    t1 = perf_counter()
    asyncio.run(fetch_stats())
    t2 = perf_counter() - t1
    print('Pokemon stats are ready. ({:.2f}s)'.format(t2))


def init_pokemon_battlefield():
    """
        Initializes the Pokémon battlefield by prompting the user to choose two Pokémon.
        Fetches data for the chosen Pokémon and creates `Pokemon` instances for them.

        Returns:
            tuple: A pair of `Pokemon` objects representing the chosen Pokémon for the battle.
        """
    print('Welcome to the Pokemon battlefield game!')
    print('Please choose your pokemons:')
    pokemon1_name = input('Pokemon 1: ')
    pokemon2_name = input('Pokemon 2: ')

    print('Preparing the pokemons...')
    pokemon1_data = fetch_data_sync(POKE_API_POKEMON, pokemon1_name)
    pokemon2_data = fetch_data_sync(POKE_API_POKEMON, pokemon2_name)

    pokemon1_obj = Pokemon(poke_id=pokemon1_data['id'],
                           name=pokemon1_data['name'],
                           moves=[x['move']['name'] for x in
                                  pokemon1_data['moves']],
                           stats={
                               x['stat']['name']: (x['base_stat'], x['effort'])
                               for x in pokemon1_data['stats']})
    pokemon2_obj = Pokemon(poke_id=pokemon2_data['id'],
                           name=pokemon2_data['name'],
                           moves=[x['move']['name'] for x in
                                  pokemon2_data['moves']],
                           stats={
                               x['stat']['name']: (x['base_stat'], x['effort'])
                               for x in pokemon2_data['stats']})

    return pokemon1_obj, pokemon2_obj


def battle(pkm1: Pokemon, pkm2: Pokemon):
    """
        Simulates a battle between two Pokémon, determining the order based on their speed.
        Continuously alternates attacks between the two Pokémon until one's HP drops to 0 or below.
        Records battle notes and handles exceptions during the battle process.

        Args:
            pkm1 (Pokemon): The first Pokémon participant in the battle.
            pkm2 (Pokemon): The second Pokémon participant in the battle.

        Prints the outcome of the battle, including the winner and any errors that occurred.
        """
    if pkm1.speed > pkm2.speed:
        attacker, defender = pkm1, pkm2
    else:
        attacker, defender = pkm2, pkm1

    print('Battle starts...')
    error_count = 0
    while True:
        try:
            # Attacker's turn
            attacker.attack(defender)
            if defender.hp <= 0:
                print(
                    f"The winner is: {attacker.name} with {attacker.hp}HP left")
                break

            # Defender's turn
            defender.attack(attacker)
            if attacker.hp <= 0:
                print(
                    f"The winner is: {defender.name} with {defender.hp}HP left")
                break
            take_battle_notes(attacker, defender)

        except Exception as e:
            print(f"An error occurred: {e.args}")
            error_count += 1
            if error_count > 3:
                print("[DRAW] Too many errors, stopping the battle.")
                print(f"{attacker.name} left with {attacker.hp}HP")
                print(f"{defender.name} left with {defender.hp}HP")
                break


if __name__ == "__main__":
    """
        Main execution block of the script.
        Initializes data and database cache, then continuously prompts the user to start a new Pokémon battle.
        Fetches initial data for Pokémon, initializes the battlefield, and conducts the battle between the chosen Pokémon.
        Records battle notes and handles exceptions.
        """
    fetch_init_data()
    init_db_cache()

    while True:
        like_to_play = input('Would you like to play?(yes/no)')

        if like_to_play.strip() == 'no':
            break

        try:
            pokemon1, pokemon2 = init_pokemon_battlefield()
            t1 = perf_counter()
            battle(pokemon1, pokemon2)
            t2 = perf_counter() - t1

            take_battle_notes(pokemon1, pokemon2, t2)
        except Exception as e:
            print(e)
