import asyncio

import aiohttp
import requests

from exceptions import FetchingError

POKE_API = 'https://pokeapi.co/api/v2'
POKE_API_ALL_STATS = f'{POKE_API}/stat'
POKE_API_POKEMON = f'{POKE_API}/pokemon/'
POKE_API_MOVE = f'{POKE_API}/move/'

CACHE_MOVES = {}

lock = asyncio.Lock()


async def fetch_data(url: str, session: aiohttp.ClientSession):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching {url}: {response.status}")
                return {}
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return {}


async def add_moves(session: aiohttp.ClientSession,
                    stat_name: str,
                    affecting_moves: list):
    for af_move in affecting_moves:
        move_name = af_move['move']['name']

        if move_name not in CACHE_MOVES:
            move_detail = await fetch_data(url=af_move['move']['url'],
                                           session=session)
            CACHE_MOVES[move_name] = {stat_name: (move_detail['power'],
                                                  af_move['change'])}
        elif stat_name not in CACHE_MOVES[move_name]:
            power = list(CACHE_MOVES[move_name].values())[0][0]
            CACHE_MOVES[move_name][stat_name] = (power,
                                                 af_move['change'])


async def process_stat(session: aiohttp.ClientSession, stat_name: str,
                       stat_url: str):
    stat = await fetch_data(url=stat_url, session=session)

    affecting_moves = (stat['affecting_moves']['increase'] +
                       stat['affecting_moves']['decrease'])

    await add_moves(session, stat_name, affecting_moves)


async def get_stats_with_moves(session: aiohttp.ClientSession):
    stats = await fetch_data(url=POKE_API_ALL_STATS,
                             session=session)
    stats = ((x['name'], x['url']) for x in stats.get('results', {}))

    await asyncio.gather(*[asyncio.create_task(process_stat(session, k, v))
                           for k, v in stats])


async def fetch_stats():
    async with aiohttp.ClientSession() as session:
        await get_stats_with_moves(session)


def fetch_data_sync(static_path, variable):
    response = requests.get(''.join([static_path, variable]))

    if response.status_code == 200:
        return response.json()
    else:
        raise FetchingError(
            f"Error fetching {response.request.url}: {response.status_code}")
