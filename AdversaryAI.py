from random import randint
from BaseAI import BaseAI

class AdversaryAI(BaseAI):
    def __init__(self):
        super().__init__()

    def get_move(self, grid):
        cells = grid.get_empty_cells()

        return cells[randint(0, len(cells) - 1)] if cells else None
