from syntax_tree import Node
types = {' ': 'FLOOR',
         'X': 'WALL',
         'E': 'EXIT'}

cells = {'EMPTY': 2,
         'WALL': 1,
         'EXIT': 0}


class Cell:
    def __init__(self, _type):
        self.type = _type
        if not _type == 'FLOOR':
            self.passwords = []
        else:
            self.passwords = None

    def __repr__(self):
        if not self.type == 'FLOOR':
            return f"{self.type}: {self.passwords}"
        else:
            return self.type


class Robot:
    def __init__(self, _x=0, _y=0, _map=None):
        self.x = _x
        self.y = _y
        self.map = _map
        self.passwords = []
        self.walls = ['WALL', 'EXIT']
        self.found_exit = False

    def __repr__(self):
        return f'Robot at [{self.x}, {self.y}]\nPasswords:\n{self.passwords}'

    def move_up(self, steps):
        while steps and (self.map[self.y][self.x + 1].type == "FLOOR"):
            self.x += 1
            steps -= 1
        return steps

    def move_down(self, steps):
        while steps and (self.map[self.y][self.x - 1].type == "FLOOR"):
            self.x -= 1
            steps -= 1
        return steps

    def move_right(self, steps):
        while steps and (self.map[self.y + 1][self.x].type == "FLOOR"):
            self.y += 1
            steps -= 1
        return steps

    def move_left(self, steps):
        while steps and (self.map[self.y - 1][self.x].type == "FLOOR"):
            self.y -= 1
            steps -= 1
        return steps

    def ping_up(self, _type):
        dist = 0
        while self.map[self.y][self.x + dist + 1].type == "FLOOR":
            dist += 1
        if not _type:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.y][self.x + dist].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.y][self.x + dist].type == "EXIT"):
            return dist
        else:
            return None

    def ping_down(self, _type):
        dist=0
        while self.map[self.y][self.x - dist - 1].type == "FLOOR":
            dist += 1
        if not _type:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.y][self.x - dist].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.y][self.x - dist].type == "EXIT"):
            return dist
        else:
            return None

    def ping_right(self, _type):
        dist=0
        while self.map[self.y + dist + 1][self.x].type == "FLOOR":
            dist+=1
        if not _type:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.y + dist][self.x].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.y + dist][self.x].type == "EXIT"):
            return dist
        else:
            return None

    def ping_left(self, _type):
        dist = 0
        while self.map[self.y - dist - 1][self.x].type == "FLOOR":
            dist += 1
        if not _type:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.y - dist][self.x].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.y - dist][self.x].type == "EXIT"):
            return dist
        else:
            return None

    def vision(self):
        pasw = []
        if self.map[self.y - 1][self.x].type == 'WALL':
            for psw in self.map[self.y - 1][self.x].passwords:
                pasw.append(psw)
        elif self.map[self.y + 1][self.x].type == 'WALL':
            for psw in self.map[self.y + 1][self.x].passwords:
                pasw.append(psw)
        elif self.map[self.y][self.x - 1].type == 'WALL':
            for psw in self.map[self.y][self.x - 1].passwords:
                pasw.append(psw)
        elif self.map[self.y][self.x + 1].type == 'WALL':
            for psw in self.map[self.y][self.x + 1].passwords:
                pasw.append(psw)
        return pasw

    def voice(self, pasw):
        if self.map[self.y - 1][self.x].type == 'EXIT':
            if pasw in self.map[self.y-1][self.x].passwords:
                self.found_exit = True
        elif self.map[self.y + 1][self.x].type == 'EXIT':
            if pasw in self.map[self.y + 1][self.x].passwords:
                self.found_exit = True
        elif self.map[self.y][self.x - 1].type == 'EXIT':
            if pasw in self.map[self.y][self.x - 1].passwords:
                self.found_exit = True
        elif self.map[self.y][self.x + 1].type == 'EXIT':
            if pasw in self.map[self.y][self.x + 1].passwords:
                self.found_exit = True
        if self.found_exit:
            print("*** EXIT FOUND, CONGRATULATIONS ***")
        else:
            print("*** YOU CAN'T LEAVE THE LABYRINTH YET ***")