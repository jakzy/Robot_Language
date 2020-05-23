from syntax_tree import Node
from os import system
from time import sleep


# as PyCharm doesnt like 'cls', a kludge here, sorry :(
def clear():
    sleep(0.2)
    print('\n'*1000)


types = {' ': 'FLOOR',
         'X': 'WALL',
         'E': 'EXIT'}

cells = {'FLOOR': 2,
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

    def show(self):
        for row in range(len(self.map)):
            for cell in range(len(self.map[row])):
                if self.map[row][cell].type == 'FLOOR':
                    if (cell == self.y) and (row == self.x):
                        print("@", end=' ')
                    else:
                        print(" ", end=' ')
                elif self.map[row][cell].type == 'EXIT':
                    print("E", end=' ')
                else:
                    print("X", end=' ')
            print()

    def move_up(self, steps):
        while steps and (self.x - 1 >= 0) and (self.map[self.x - 1][self.y].type == "FLOOR"):
            self.x -= 1
            print(steps, '/\\')
            self.show()
            clear()
            steps -= 1
        return steps

    def move_down(self, steps):
        while steps and (self.x + 1 < len(self.map)) and (self.map[self.x + 1][self.y].type == "FLOOR"):
            self.x += 1
            print(steps, '\\/')
            self.show()
            clear()
            steps -= 1
        return steps

    def move_right(self, steps):
        while steps and (self.y + 1 < len(self.map[self.x])) and (self.map[self.x][self.y + 1].type == "FLOOR"):
            self.y += 1
            print(steps, '>')
            self.show()
            clear()
            steps -= 1
        return steps

    def move_left(self, steps):
        while steps and (self.y - 1 >= 0) and (self.map[self.x][self.y - 1].type == "FLOOR"):
            self.y -= 1
            print(steps, '<')
            self.show()
            clear()
            steps -= 1
        return steps

    def ping_up(self, _type):
        dist = 0
        while self.map[self.x - dist - 1][self.y].type == "FLOOR":
            dist += 1
        if _type is None:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.x - dist][self.y].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.x - dist][self.y].type == "EXIT"):
            return dist
        else:
            return None

    def ping_down(self, _type):
        dist = 0
        while self.map[self.x + dist + 1][self.y].type == "FLOOR":
            dist += 1
        if _type is None:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.x + dist][self.y].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.x + dist][self.y].type == "EXIT"):
            return dist
        else:
            return None

    def ping_right(self, _type):
        dist = 0
        while self.map[self.x][self.y + dist + 1].type == "FLOOR":
            dist += 1
        if _type is None:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.x][self.y + dist].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.x][self.y + dist].type == "EXIT"):
            return dist
        else:
            return None

    def ping_left(self, _type):
        dist = 0
        while self.map[self.x][self.y - dist - 1].type == "FLOOR":
            dist += 1
        if _type is None:
            return dist
        elif (_type == cells['WALL']) and (self.map[self.x][self.y - dist].type == "WALL"):
            return dist
        elif (_type == cells['EXIT']) and (self.map[self.x][self.y - dist].type == "EXIT"):
            return dist
        else:
            return None

    def vision(self):
        pasw = []
        if self.map[self.x][self.y - 1].type == 'WALL':
            for psw in self.map[self.x][self.y - 1].passwords:
                pasw.append(psw)
        if self.map[self.x][self.y + 1].type == 'WALL':
            for psw in self.map[self.x][self.y + 1].passwords:
                pasw.append(psw)
        if self.map[self.y][self.x - 1].type == 'WALL':
            for psw in self.map[self.x - 1][self.y].passwords:
                pasw.append(psw)
        if self.map[self.x + 1][self.y].type == 'WALL':
            for psw in self.map[self.x + 1][self.y].passwords:
                pasw.append(psw)
        return pasw

    def voice(self, pasw):
        if self.map[self.x][self.y - 1].type == 'EXIT':
            if pasw in self.map[self.x][self.y-1].passwords:
                self.found_exit = True
        if self.map[self.x][self.y + 1].type == 'EXIT':
            if pasw in self.map[self.x][self.y + 1].passwords:
                self.found_exit = True
        if self.map[self.x - 1][self.y].type == 'EXIT':
            if pasw in self.map[self.x - 1][self.y].passwords:
                self.found_exit = True
        if self.map[self.x + 1][self.y].type == 'EXIT':
            if pasw in self.map[self.x + 1][self.y].passwords:
                self.found_exit = True
        if self.found_exit:
            print("*** THE PASSWORD IS CORRECT, EXIT FOUND, CONGRATULATIONS ***")
        else:
            print("*** YOU CAN'T LEAVE THE LABYRINTH YET ***")