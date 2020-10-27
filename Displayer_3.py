from BaseDisplayer_3 import BaseDisplayer
import platform
import os

# style, foreground, background
colorMap = {
    0: [0, 30, 40],
    2: [0, 37, 40],
    4: [0, 36, 40],
    8: [0, 35, 40],
    16: [0, 34, 40],
    32: [0, 33, 40],
    64: [0, 32, 40],
    128: [0, 31, 40],
    256: [0, 30, 104],
    512: [0, 30, 105],
    1024: [0, 30, 46],
    2048: [0, 30, 42],
    4096: [0, 30, 102],
    8192: [0, 30, 103],
    16384: [0, 30, 105],
    32768: [0, 30, 106],
    65536: [0, 20, 101],
}

cTemp = "\033[%sm%7s\033[0m "

class Displayer(BaseDisplayer):
    def __init__(self):
        super().__init__()
        if "Windows" == platform.system():
            self.display = self.windows_display
        else:
            self.display = self.unix_display

    def display(self, grid):
        pass

    @staticmethod
    def windows_display(grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")

    @staticmethod
    def unix_display(grid):
        for i in range(3 * grid.size):
            for j in range(grid.size):
                v = grid.map[int(i / 3)][j]

                if i % 3 == 1:
                    string = str(v).center(7, " ")
                else:
                    string = " "

                color = ";".join([str(colorMap[v][0]), str(colorMap[v][1]), str(colorMap[v][2])])
                print(cTemp % (color, string), end="")
            print("")

            if i % 3 == 2:
                print("")
