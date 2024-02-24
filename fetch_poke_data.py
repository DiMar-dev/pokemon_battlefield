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
    """
        Asynchronously fetches JSON data from a given URL using aiohttp session.

        Args:
            url (str): The URL from which data is to be fetched.
            session (aiohttp.ClientSession): The aiohttp session to be used for making the request.

        Returns:
            dict: The JSON data fetched from the URL. Returns an empty dict if the fetch fails.
        """
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
    """
        Asynchronously adds move details to the CACHE_MOVES dictionary for a given stat.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to be used for making the request.
            stat_name (str): The name of the stat for which moves are being added.
            affecting_moves (list): A list of moves that are part of a stat.

        This function updates the global CACHE_MOVES dictionary with move details.
        """
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
    """
        Processes a single stat by fetching its details and the moves affecting it.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to be used for making requests.
            stat_name (str): The name of the stat to process.
            stat_url (str): The URL to fetch the stat details from.

        This function fetches stat details and updates the CACHE_MOVES with moves affecting this stat.
        """
    stat = await fetch_data(url=stat_url, session=session)

    affecting_moves = (stat['affecting_moves']['increase'] +
                       stat['affecting_moves']['decrease'])

    await add_moves(session, stat_name, affecting_moves)


async def get_stats_with_moves(session: aiohttp.ClientSession):
    """
        Fetches all stats and their affecting moves, updating CACHE_MOVES with the details.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to be used for making requests.

        This function fetches all stats and then processes each stat to update CACHE_MOVES with move details.
        """
    stats = await fetch_data(url=POKE_API_ALL_STATS,
                             session=session)
    stats = ((x['name'], x['url']) for x in stats.get('results', {}))

    await asyncio.gather(*[asyncio.create_task(process_stat(session, k, v))
                           for k, v in stats])


async def fetch_stats():
    """
        Initiates the process of fetching all stats and their affecting moves using an aiohttp session.

        This function creates an aiohttp session and calls get_stats_with_moves to populate CACHE_MOVES.
        """
    async with aiohttp.ClientSession() as session:
        await get_stats_with_moves(session)


def fetch_data_sync(static_path, variable):
    """
        Synchronously fetches JSON data by constructing a URL from a static path and a variable component.

        Args:
            static_path (str): The static part of the URL.
            variable (str): The variable component of the URL to be appended to the static path.

        Returns:
            dict: The JSON data fetched from the constructed URL.

        Raises:
            FetchingError: If the fetch operation fails with a non-200 status code.
        """
    response = requests.get(''.join([static_path, variable]))

    if response.status_code == 200:
        return response.json()
    else:
        raise FetchingError(
            f"Error fetching {response.request.url}: {response.status_code}")
