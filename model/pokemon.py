import random

from model.affecting_move import AffectingMove
from exceptions import StatsMissMatchError
from fetch_poke_data import CACHE_MOVES, fetch_data_sync, \
    POKE_API_MOVE
from model.move import Move

ATTACK = 'attack'
DEFENSE = 'defense'


class Pokemon:
    """
        Represents a Pokémon with its basic attributes and functionality for battling.

        Attributes:
            poke_id (int): Unique identifier for the Pokémon.
            name (str): Name of the Pokémon.
            moves (list): List of moves (as strings) the Pokémon can perform.
            hp (float): Health points of the Pokémon.
            speed (float): Speed stat of the Pokémon, determining turn order in battles.
            stats (dict): Dictionary containing various stats of the Pokémon, e.g., {'stat_name': (base_stat, effort)}.
            current_attack (AffectingMove): The current move set for an attack, represented as an AffectingMove instance.
            attacks (list): List of AffectingMove instances representing moves the Pokémon has used.

        Methods:
            set_current_move: Sets the current move for the Pokémon from its list of possible moves, considering the move type.
            attack: Executes an attack on an opponent Pokémon, calculating and applying damage.
        """
    def __init__(self, poke_id: int, name: str, moves: list, stats: dict):
        self.poke_id = poke_id
        self.name = name
        self.moves = moves
        self.hp = stats['hp'][0]
        self.speed = stats['speed'][0]
        self.stats = stats  # {'stat.name': (baste_stat, effort), ...}
        self.current_attack: AffectingMove = None
        self.attacks = []

    def set_current_move(self, attack_type: str):
        """
            Randomly selects a move from the Pokémon's move list and sets it as the current attack. If the move has already been used,
            it retrieves the corresponding AffectingMove instance; otherwise, it creates a new one.

            Args:
                attack_type (str): The type of attack to set, either 'attack' or 'defense', affecting the choice of move.

            Raises:
                StatsMissMatchError: If there's a mismatch between the move's expected stats and the Pokémon's actual stats.
            """
        move_name = random.choice(self.moves)

        if self.current_attack and move_name == self.current_attack.move.name:
            return
        elif any(x.move.name == move_name for x in self.attacks):
            self.current_attack = [x for x in self.attacks
                                   if x.move.name == move_name][0]
            return

        if move_name in CACHE_MOVES:
            stat_name = None
            if isinstance(CACHE_MOVES[move_name], dict):
                common_stats = (set(CACHE_MOVES[move_name].keys())
                                & set(self.stats.keys()))
                stat_name = next((key for key in common_stats
                                  if attack_type in key), None)
                stat_name = stat_name or next(iter(common_stats), None)
                if stat_name is None:
                    raise StatsMissMatchError(f'Stats missmatch for pokemon {self.name} and move {move_name}')

            if stat_name:
                power, change = CACHE_MOVES[move_name][stat_name]
                self.current_attack = AffectingMove(
                    stat_type=stat_name,
                    base_stat=self.stats[stat_name][0],
                    effort_ev=self.stats[stat_name][1],
                    move=Move(name=move_name, power=power, change=change))
            else:
                power, change = CACHE_MOVES[move_name]
                self.current_attack = AffectingMove(
                    stat_type=None,
                    base_stat=1,
                    effort_ev=1,
                    move=Move(name=move_name, power=power, change=change))
        else:
            move = fetch_data_sync(POKE_API_MOVE, move_name)
            self.current_attack = AffectingMove(
                stat_type=None,
                base_stat=1,
                effort_ev=1,
                move=Move(name=move_name, power=move['power'], change=0))
            CACHE_MOVES[move_name] = (move['power'], 0)
        self.attacks.append(self.current_attack)

    def attack(self, opponent):
        """
            Performs an attack on an opponent Pokémon. This method sets the current move for both the attacking and defending Pokémon,
            calculates the damage using the `attacking_damage` method from AffectingMove, and applies it to the opponent's HP.

            Args:
                opponent (Pokemon): The opponent Pokémon being attacked.
            """
        self.set_current_move(ATTACK)
        opponent.set_current_move(DEFENSE)

        damage = self.current_attack.attacking_damage(opponent.current_attack)
        opponent.hp -= damage
