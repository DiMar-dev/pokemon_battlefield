import random

from move import Move


class AffectingMove:
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
        self.stat_changed = \
            ((((2 * self.stat_changed + self.iv + (
                        self.effort_ev // 4)) * self.level) // 100 + 5)
             * self.nature_modifier)

    def apply_baste_stat_change(self):
        decreases = (0.667, 0.5, 0.4, 0.333, 0.285, 0.25)
        if self.move.change > 0:
            self.stat_changed *= (1 + 0.5 * self.move.change)
        if self.move.change < 0:
            self.stat_changed *= decreases[abs(self.move.change) - 1]

    def attacking_damage(self, defense):
        self.apply_baste_stat_change()
        defense.apply_baste_stat_change()

        if self.move.power is None:
            return 0

        damage = (((((2 * self.level) / 5 + 2) *
                    self.move.power * self.stat_changed / defense.stat_changed)
                   / 50) + 2)
        damage *= random.uniform(0.85, 1.0)
        return damage
