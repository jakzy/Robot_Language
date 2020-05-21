from syntax_tree import Node

class Robot:
    def __init__(self, _x=0, _y=0, _map=None):
        self.x = _x
        self.y = _y
        self.map = _map
        self.passwords = []

    def __repr__(self):
        return f'Robot at [{self.x}, {self.y}]\nPasswords:\n{self.passwords}'

    def move_up(self, steps):
        pass

    def move_down(self, steps):
        pass

    def move_right(self, steps):
        pass

    def move_left(self, steps):
        pass

    def ping_up(self, res):
        pass

    def ping_down(self, res):
        pass

    def ping_right(self, res):
        pass

    def ping_left(self, res):
        pass

    def vision(self, pasw):
        pass

    def voice(self, pasw):
        # the curr cell is an exit?
        # # TRUE
        # # is the password correct?
        # # # TRUE
        # # # leave the labirint
        # return
        pass
