from copy import deepcopy

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class Grid:
    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for _i in range(self.size)]

    def clone(self):
        grid_copy = Grid()
        grid_copy.map = deepcopy(self.map)
        grid_copy.size = self.size

        return grid_copy

    def insert_tile(self, pos, value):
        self.set_cell_value(pos, value)

    def set_cell_value(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def get_empty_cells(self):
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x, y))

        return cells

    def get_max_tile(self):
        max_tile = 0

        for x in range(self.size):
            for y in range(self.size):
                max_tile = max(max_tile, self.map[x][y])

        return max_tile

    def can_insert(self, pos):
        return self.get_cell_value(pos) == 0

    def move(self, dir):
        dir = int(dir)

        if dir == UP:
            return self.do_move(True, False)
        if dir == DOWN:
            return self.do_move(True, True)
        if dir == LEFT:
            return self.do_move(False, False)
        if dir == RIGHT:
            return self.do_move(False, True)

    def do_move(self, is_horizontal, is_positive):
        """
        Perform the actual move
        :param is_horizontal: If the move is horizontal or vertical
        :param is_positive: Depending on is_horizontal, positive is left or up, negative is down or right
        :return:
        """
        rng = range(self.size - 1, -1, -1) if is_positive else range(self.size)

        moved = False

        for pos_one in range(self.size):
            cells = []

            for pos_two in rng:
                cell = self.map[pos_two][pos_one] if is_horizontal else self.map[pos_one][pos_two]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for pos_two in rng:
                value = cells.pop(0) if cells else 0

                if is_horizontal:
                    if self.map[pos_two][pos_one] != value:
                        moved = True
                    self.map[pos_two][pos_one] = value
                else:
                    if self.map[pos_one][pos_two] != value:
                        moved = True
                    self.map[pos_one][pos_two] = value

        return moved

    @staticmethod
    def merge(cells):
        if len(cells) <= 1:
            return cells

        cell = 0
        while cell < len(cells) - 1:
            if cells[cell] == cells[cell + 1]:
                cells[cell] *= 2
                del cells[cell + 1]
            cell += 1

    def can_move(self, dirs=vecIndex):
        checking_moves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y]:
                    for move in checking_moves:
                        move = directionVectors[move]
                        adj_cell_value = self.get_cell_value((x + move[0], y + move[1]))
                        if adj_cell_value == self.map[x][y] or adj_cell_value == 0:
                            return True
                elif self.map[x][y] == 0:
                    return True

        return False

    def get_available_moves(self, dirs=vecIndex):
        available_moves = []

        for x in dirs:
            grid_copy = self.clone()

            if grid_copy.move(x):
                available_moves.append(x)

        return available_moves

    def cross_bound(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    def get_cell_value(self, pos):
        if not self.cross_bound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

if __name__ == '__main__':
    g = Grid()
    g.map[0][0] = 2
    g.map[1][0] = 2
    g.map[3][0] = 4

    while True:
        for i in g.map:
            print(i)
        print(g.get_available_moves())
        v = input()
        g.move(v)
