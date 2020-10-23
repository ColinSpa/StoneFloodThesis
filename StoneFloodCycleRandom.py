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

            if cycle_color == 5:
                cycle_color = 0
        self.print()
        print("the number of steps taken is " + str(cycle_steps))


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

        self.print()
        print("the number of steps taken is " + str(random_steps))


class Greedy(Board):

    def __init__(self, M, N):
        super().__init__(M, N)

    def field_size(self, to_color):
        from_color = self.fields[(0, 0)].color
        tiles_changed = 0
        to_be_changed = set([self.fields[(0, 0)]])
        while to_be_changed:
            field = to_be_changed.pop()
            to_be_changed |= set([f for f in field.neighbors if f.color == from_color])
            field.color = to_color  # update kleur
            tiles_changed += 1
        return tiles_changed

    '''field_size uses the same code as make_move, except that it now counts the number of tiles of the main field and
     returns this value. In the most_tiles_added method below, field_size is used to count the tiles added to the main 
     field when a move is made. This is done by taking the difference between the initial field and the field after the 
     color change. Most_tiles_added returns the color which returns the most tiles. '''

    def most_tiles_added(self):
        greedy_colors = np.zeros(self.num_colors)
        for i in range(self.num_colors):
            test = copy.deepcopy(self)
            from_color = test.fields[(0, 0)].color
            if i == from_color:
                greedy_colors[i] = 0
            else:
                greedy_colors[i] = abs(test.field_size(i) - test.field_size(self.num_colors + 1))

        return greedy_colors.tolist().index(max(greedy_colors))

    '''greedy_heur applies the greedy heuristic where the color chosen is the color which adds the most tiles in a 
        single step. It returns the number of steps taken.'''

    def greedy_heur(self):
        greedy_steps = 0
        while not self.check():
            greedy_col = self.most_tiles_added()
            self.make_move(greedy_col)
            greedy_steps += 1

        self.print()
        print("the number of steps taken is " + str(greedy_steps))


board = Random(7, 7)
board.make_fields()
board.print()
board.apply_random()

board = Cycle(7, 7)
board.make_fields()
board.print()
board.apply_cycle()

board = Greedy(7, 7)
board.make_fields()
board.print()
board.greedy_heur()
