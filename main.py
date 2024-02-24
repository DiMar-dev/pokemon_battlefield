import asyncio
from time import perf_counter

from fetch_poke_data import fetch_stats, fetch_data_sync, \
    POKE_API_POKEMON
from pokemon import Pokemon


def fetch_init_data():
    print('Loading pokemon data...')
    t1 = perf_counter()
    asyncio.run(fetch_stats())
    t2 = perf_counter() - t1
    print('Pokemon stats are ready. ({:.2f}s)'.format(t2))


def init_pokemon_battlefield():
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


def battle(pkm1, pkm2):
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

        except Exception as e:
            print(f"An error occurred: {e.args}")
            error_count += 1
            if error_count > 3:
                print("[DRAW] Too many errors, stopping the battle.")
                print(f"{attacker.name} left with {attacker.hp}HP")
                print(f"{defender.name} left with {defender.hp}HP")
                break


if __name__ == "__main__":
    fetch_init_data()

    while True:
        like_to_play = input('Would you like to play?(yes/no)')

        if like_to_play == 'no':
            break

        try:
            pokemon1, pokemon2 = init_pokemon_battlefield()
            battle(pokemon1, pokemon2)
        except Exception as e:
            print(e)
