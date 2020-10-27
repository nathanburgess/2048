from BaseAI import BaseAI
from collections import OrderedDict
from functools import reduce
from itertools import chain
from time import clock
from math import pow, exp

class PlayerAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.start_time = 0
        self.weights = [[-3.8, -3.7, -3.5, -3],
                        [-.5, -1.5, -1.8, -2],
                        [1, 1, 1, 1],
                        [15, 12.5, 7, 6.5]]
        self.weights = [[exp(self.weights[i][j]) for j in range(4)] for i in range(4)]
        self.weights_flat = list(chain(*self.weights))

        self.depth = 0
        self.max_depth = 5
        self.start_time = 0
        self.max_run_time = 0.1

        self.mono_incr = lambda l: reduce(lambda a, b: b if a <= b else float("inf"), l) != float("inf")
        self.mono_decr = lambda l: reduce(lambda a, b: b if a >= b else -float("inf"), l) != -float("inf")
        self.man_dist = lambda l: (abs(l[0][0] - l[1][0]) + abs(l[0][1] - l[1][1]))

    def gen_children(self, state):
        moves = state.get_available_moves()
        children = OrderedDict()
        for move in moves:
            child = state.clone()
            child.move(move)
            child.direction = move
            children[self.eval(child)] = child
        children = sorted(children.items(), key=lambda x: x[0])
        return children

    def find_min(self, state, alpha, beta):
        if not state.get_available_moves() or clock() - self.start_time > self.max_run_time:
            return None, self.eval(state)

        min_child, min_utility = None, float("inf")
        self.depth += 1

        for util, child in self.gen_children(state):
            if self.depth > self.max_depth or clock() - self.start_time > self.max_run_time:
                utility = util
            else:
                utility = self.chance(child, alpha, beta, self.find_max)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

        return min_child, min_utility

    def find_max(self, state, alpha, beta):
        if not state.get_available_moves() or clock() - self.start_time > self.max_run_time:
            return None, self.eval(state)

        max_child, max_utility = None, -float("inf")
        self.depth += 1

        children = list(reversed(self.gen_children(state)))
        for util, child in children:
            if self.depth > self.max_depth or clock() - self.start_time > self.max_run_time:
                utility = util
            else:
                utility = self.chance(child, alpha, beta, self.find_min)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return max_child, max_utility

    def chance(self, state, alpha, beta, search_fn):
        blanks = state.get_empty_cells()
        children2 = set()
        children4 = set()
        for spot in blanks:
            child = state.clone()
            child.insert_tile(spot, 2)
            children2.add(child)
            child = state.clone()
            child.insert_tile(spot, 4)
            children4.add(child)

        utilities2 = utilities4 = []

        for child in children2:
            if self.depth > self.max_depth or clock() - self.start_time > self.max_run_time:
                utility = self.eval(child)
            else:
                _, utility = search_fn(child, alpha, beta)

            utilities2.append(utility)
        for child in children4:
            if self.depth > self.max_depth or clock() - self.start_time > self.max_run_time:
                utility = self.eval(child)
            else:
                _, utility = search_fn(child, alpha, beta)
            utilities4.append(utility)

        return (sum(utilities2) / len(utilities2) * 0.9) + \
               (sum(utilities4) / len(utilities4) * 0.1)

    def get_move(self, grid):
        """
        Return the selected move to the GameManager
        """
        self.start_time = clock()
        move, util = self.find_max(grid, -float("inf"), float("inf"))
        return move.direction

    @staticmethod
    def edge_bonus(state):
        value = 0
        for i in range(4):
            value += (state[3][i] + state[i][0])
        return value

    @staticmethod
    def adjacency_bonus(state):
        value = 0
        for i in range(4):
            for j in range(4):
                if j < 3 and state[i][j] == state[i][j + 1]:
                    value += state[i][j]
                if i < 3 and state[i][j] == state[i + 1][j]:
                    value += state[i][j]
        return value

    def mono_bonus(self, state):
        value = 0
        for x in range(4):
            col = [state[i][x] for i in range(4)]
            row = state[x]
            if self.mono_incr(col):
                value += sum(col)
            if self.mono_decr(row):
                value += sum(row)
        return value

    @staticmethod
    def dot_product(a, b):
        total = 0
        for i in range(4):
            for j in range(4):
                total += a[i][j] * b[i][j]
        return total

    def eval(self, state):
        utility = 0
        state_flat = list(chain(*state.map))
        num_blanks = state_flat.count(0)

        h_blanks = pow(num_blanks, 3)
        h_weight = self.dot_product(self.weights, state.map)
        h_adjacent = (self.adjacency_bonus(state.map))
        h_mono = (self.mono_bonus(state.map))
        h_adjacent *= 303.456

        utility += h_weight
        utility += h_blanks * sum(state_flat) - max(state_flat)
        utility += h_adjacent
        utility += h_mono

        return utility
