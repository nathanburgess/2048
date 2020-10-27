from Grid_3 import Grid
from AdversaryAI import AdversaryAI
from PlayerAI import PlayerAI
from Displayer_3 import Displayer
from random import randint
import time

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

class GameManager:
    def __init__(self, size=4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles = defaultInitialTiles
        self.adversary_ai = None
        self.player_ai = None
        self.displayer = None
        self.over = False

    def set_adversary_ai(self, ai):
        self.adversary_ai = ai

    def set_player_ai(self, ai):
        self.player_ai = ai

    def set_displayer(self, displayer):
        self.displayer = displayer

    def start(self):
        for _ in range(self.initTiles):
            self.insert_random_tile()

        turn = PLAYER_TURN
        max_tile = 0

        while not self.is_game_over() and not self.over:
            grid_copy = self.grid.clone()

            if turn == PLAYER_TURN:
                move = self.player_ai.get_move(grid_copy)

                if move is not None and 0 <= move < 4:
                    if self.grid.can_move([move]):
                        self.grid.move(move)

                        max_tile = self.grid.get_max_tile()
                    else:
                        self.over = True
                else:
                    self.over = True
            else:
                move = self.adversary_ai.get_move(grid_copy)

                if move and self.grid.can_insert(move):
                    self.grid.set_cell_value(move, self.get_new_tile_value())
                else:
                    self.over = True

            if not self.over:
                self.displayer.display(self.grid)

            turn = 1 - turn

        print("The program achieved a maximum tile value of %d" % max_tile)

    def is_game_over(self):
        return not self.grid.can_move()

    def get_new_tile_value(self):
        if randint(0, 99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    def insert_random_tile(self):
        tile_value = self.get_new_tile_value()
        cells = self.grid.get_empty_cells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.set_cell_value(cell, tile_value)

def main():
    game_manager = GameManager()
    player_ai = PlayerAI()
    computer_ai = AdversaryAI()
    displayer = Displayer()

    game_manager.set_displayer(displayer)
    game_manager.set_player_ai(player_ai)
    game_manager.set_adversary_ai(computer_ai)

    game_manager.start()

if __name__ == '__main__':
    main()
