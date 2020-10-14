import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5)


class Field:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.neighbors = set()

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.color}"


class Board:
    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.fields = {}
        self.num_colors = 5
        self.colors = np.random.randint(self.num_colors, size=(self.M, self.N))

    def make_fields(self):
        for x in range(self.M):
            for y in range(self.N):
                self.fields[(x, y)] = Field(x, y, self.colors[x, y])

        for x in range(self.M):
            for y in range(self.N):
                neighbors = set([(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)])
                self.fields[(x, y)].neighbors = set(
                    [
                        self.fields[n]
                        for n in neighbors
                        if (0 <= n[0] < self.M and 0 <= n[1] < self.N)  # **
                    ]
                )

    def make_move(self, to_color):
        from_color = self.fields[(0, 0)].color
        if to_color == from_color:
            print("to color is equal to from color")
            quit()
        to_be_changed = set([self.fields[(0, 0)]])
        while to_be_changed:
            field = to_be_changed.pop()
            to_be_changed |= set([f for f in field.neighbors if f.color == from_color])
            field.color = to_color  # update kleur

    def print(self):
        A = np.zeros((self.M, self.N))
        for x in range(self.M):
            for y in range(self.N):
                A[x, y] = self.fields[(x, y)].color
        print(A)

    def check(self):
        B = np.zeros(self.M*self.N)
        for x in range(board.M):
            for y in range(board.N):
               B[self.M*x + y] = board.fields[(0, 0)].color == board.fields[(x, y)].color
        return all(B)

    def cycle(self):
        cycle_color = board.fields[(0,0)].color + 1  #voorkomt dat to_color == from_color
        cycle_steps = 0
        while not board.check():
            self.make_move(cycle_color)
            cycle_color += 1
            cycle_steps += 1

            if cycle_color == 5:
                cycle_color = 0
        board.print()
        print("the number of steps taken is " + str(cycle_steps))

    def random(self):
        random_color = np.random.randint(5, size=1)
        random_steps = 0

        while not board.check():
            while board.fields[(0,0)].color == random_color:
                random_color = np.random.randint(5, size=1)  #voorkomt dat to_color == from_color

            self.make_move(random_color)
            random_color = np.random.randint(5, size=1)
            random_steps += 1

        board.print()
        print("the number of steps taken is " + str(random_steps))

""" Met de method check wordt gecheckt of alle kleuren gelijk zijn. Als dat het geval is geef de functie True als 
output. The cycle en random methods gebruiken de check method als condition in de while not loop. """

board = Board(10, 10)
board.make_fields()
board.print()

board.cycle()

board = Board(10, 10)
board.make_fields()
board.print()

board.random()


