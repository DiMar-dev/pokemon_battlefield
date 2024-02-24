

class Move:

    def __init__(self, name: str, power: int, change: int):
        self.name = name
        self.power = power
        self.change = change

    def details(self):
        return f'Move({self.name}, {self.power}, {self.change})'
