import random

from model.move import Move


class AffectingMove:
    """
        Represents a move's effect on a Pokémon's stat, incorporating various factors like base stats, IVs, EVs, and nature.

        Attributes:
            stat_type (str): The type of stat affected by the move (e.g., 'attack', 'defense').
            stat_changed (float): The base stat that is modified by the move.
            effort_ev (int): The effort values (EVs) associated with the stat.
            move (Move): The move causing the stat change.
            iv (float): The individual values (IVs), randomly determined for the stat.
            level (int): The level of the Pokémon, affecting the stat calculation.
            nature_modifier (float): A modifier based on the Pokémon's nature, affecting the stat.

        Methods:
            calculate_stat: Recalculates the `stat_changed` attribute considering base stat, IVs, EVs, level, and nature.
            apply_baste_stat_change: Applies the move's effect on the stat, adjusting `stat_changed` based on the move's power.
            attacking_damage: Calculates the damage dealt by an attack, considering the defender's modified stats.
        """
    def __init__(self, stat_type: str, base_stat: float, effort_ev: int, move: Move):
        self.stat_type = stat_type  # ['attack' | 'defense', ...]
        self.stat_changed = base_stat
        self.effort_ev = effort_ev
        self.move: Move = move
        self.iv = random.uniform(0, 15)
        self.level = 1
        self.nature_modifier = random.uniform(0.85, 1.0)

        if stat_type:
            self.calculate_stat()

    def calculate_stat(self):
        """
            Recalculates the modified stat value considering base stat, IVs, EVs, level, and nature modifier. This method updates
            the `stat_changed` attribute based on these factors, following the Pokémon stat calculation formula.
            """
        self.stat_changed = \
            ((((2 * self.stat_changed + self.iv + (
                        self.effort_ev // 4)) * self.level) // 100 + 5)
             * self.nature_modifier)

    def apply_baste_stat_change(self):
        """
            Applies the base stat change induced by the move. If the move increases the stat, it's boosted by a factor related
            to the move's change value. If the move decreases the stat, it's reduced according to a predefined decrease scale.
            This method updates the `stat_changed` attribute accordingly.
            """
        decreases = (0.667, 0.5, 0.4, 0.333, 0.285, 0.25)
        if self.move.change > 0:
            self.stat_changed *= (1 + 0.5 * self.move.change)
        if self.move.change < 0:
            self.stat_changed *= decreases[abs(self.move.change) - 1]

    def attacking_damage(self, defense) -> float:
        """
            Calculates the damage dealt by this move to a defender, considering the current modified stats of both the attacker
            and the defender.

            Args:
                defense (AffectingMove): The defending Pokémon's corresponding `AffectingMove` instance, representing its defense stat.

            Returns:
                float: The calculated damage based on the move's power, the attacker's and defender's modified stats, and random
                       factors to introduce variability.
            """
        self.apply_baste_stat_change()
        defense.apply_baste_stat_change()

        if self.move.power is None:
            return 0

        damage = (((((2 * self.level) / 5 + 2) *
                    self.move.power * self.stat_changed / defense.stat_changed)
                   / 50) + 2)
        damage *= random.uniform(0.85, 1.0)
        return damage
