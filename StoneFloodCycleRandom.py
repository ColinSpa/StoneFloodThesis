import numpy as np
import matplotlib.pyplot as plt
import copy

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
        A = np.zeros((self.M, self.N))
        for x in range(self.M):
            for y in range(self.N):
                A[x, y] = self.fields[(x, y)].color
        return (self.fields[(0, 0)].color * np.ones([self.M, self.N]) == A).all()


class Cycle(Board):
    def __init__(self, M, N):
        super().__init__(M, N)

    def apply_cycle(self):
        cycle_color = self.fields[(0, 0)].color + 1
        cycle_steps = 0
        while not self.check():
            self.make_move(cycle_color)
            cycle_color += 1
            cycle_steps += 1

            if cycle_color == self.num_colors + 1:
                cycle_color = 0

        return cycle_steps


class Random(Board):
    def __init__(self, M, N):
        super().__init__(M, N)

    def apply_random(self):
        random_color = np.random.randint(5, size=1)
        random_steps = 0

        while not self.check():
            while self.fields[(0, 0)].color == random_color:
                random_color = np.random.randint(5, size=1)

            self.make_move(random_color)
            random_color = np.random.randint(5, size=1)
            random_steps += 1

        return random_steps


class Greedy(Board):

    def __init__(self, M, N):
        super().__init__(M, N)

    def apply_greedy(self):
        greedy_steps = 0
        while not self.check():
            greedy_tiles_added = np.zeros(self.num_colors)
            for i in range(self.num_colors):
                test = copy.deepcopy(self)  # copy the board so no changes are made to the actual board
                from_color = test.fields[(0, 0)].color
                if i == from_color:
                    greedy_tiles_added[i] = 0  # choosing the same color always adds 0 tiles
                else:
                    to_be_changed = set([test.fields[(0, 0)]])
                    added_tiles = set([])
                    while to_be_changed:  # while loop that adds the neighbors of the flooded area with the to_color to the set added_tiles
                        field = to_be_changed.pop()
                        to_be_changed |= set([f for f in field.neighbors if f.color == from_color])
                        added_tiles |= set([f for f in field.neighbors if f.color == i])
                        field.color = test.num_colors + 1
                    while added_tiles:  # while loop that counts the number of added tiles
                        added = added_tiles.pop()
                        added_tiles |= set([f for f in added.neighbors if f.color == i])
                        added.color = test.num_colors + 1
                        greedy_tiles_added[i] += 1

            self.make_move(greedy_tiles_added.tolist().index(max(greedy_tiles_added)))  # make the move that adds the most tiles
            greedy_steps += 1
        return greedy_steps



it = 100
steps_greedy = np.zeros(it)

for i in range(it):
    board = Greedy(1, 10)
    board.make_fields()

    steps_greedy[i] = board.apply_greedy()

print(np.mean(steps_greedy))

