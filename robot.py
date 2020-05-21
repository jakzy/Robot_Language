class Robot:
    def __init__(self, _x, _y, _map):
        self.x = _x
        self.y = _y
        self.map = _map
        self.passwords = []

    def __repr__(self):
        return f'Robot at [{self.x}, {self.y}]\nPasswords:\n{self.passwords}'
