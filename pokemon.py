import random

from affecting_move import AffectingMove
from exceptions import StatsMissMatchError
from fetch_poke_data import CACHE_MOVES, fetch_data_sync, \
    POKE_API_MOVE
from move import Move

ATTACK = 'attack'
DEFENSE = 'defense'


class Pokemon:
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
        self.set_current_move(ATTACK)
        opponent.set_current_move(DEFENSE)

        damage = self.current_attack.attacking_damage(opponent.current_attack)
        opponent.hp -= damage
