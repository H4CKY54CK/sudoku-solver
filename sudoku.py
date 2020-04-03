"""
This script was heavily cluttered before, so I decided to, at the very least,
clean up the dunders. I'm much happier with what I have now. I guess the next
thing to do is clean up the rest of it...
"""


import sys
import time
import numpy as np
from copy import copy
from sudoku_puzzles import puzzles
from collections import defaultdict
# Personal package
try:
    from misctools.timer import timeit
except:
    pass

class Sudoku:
    """Sudoku solver."""

    def __init__(self, seq):

        self._seq = seq
        self.grid = np.array([int(i) for i in list(seq)]).reshape(9,9)
        self.dmap = defaultdict(list)

    def __repr__(self):

        return f"{self.__class__.__name__}('{self._seq}')"

    def __str__(self):

        return str(self.grid)

    def possible(self, x, y, n):

        for i in range(9):
            if self.grid[x][i] == n:
                return False
        for i in range(9):
            if self.grid[i][y] == n:
                return False
        xx = (x//3)*3
        yy = (y//3)*3
        for i in range(3):
            for j in range(3):
                if self.grid[xx+j][yy+i] == n:
                    return False

        return True

    def solve(self):
        while 0 in [self.grid[x][y] for x in range(9) for y in range(9)]:
            sgrid = self.grid
            before = [sgrid[x][y] for x in range(9) for y in range(9)].count(0)
            for y in range(9):
                for x in range(9):
                    if sgrid[x][y] == 0:
                        for n in range(1,10):
                            if self.possible(x, y, n):
                                self.dmap[f"{y},{x}"].append(n)
            for key, value in self.dmap.items():
                if len(value) == 1:
                    y = int(key[0])
                    x = int(key[2])
                    sgrid[x][y] = value[0]
                    self.dmap[key].remove(value[0])
            self.dmap.clear()
            after = [sgrid[x][y] for x in range(9) for y in range(9)].count(0)
            if 0 not in [sgrid[x][y] for x in range(9) for y in range(9)]:
                return self.verify()
            elif before - after == 0:
                grid = copy(sgrid)
                sgrid = self.backup_solver()
                if np.array_equal(grid, sgrid):
                    return False


    def backup_solver(self):

        grid = [['' for x in range(9)] for y in range(9)]

        def row(x):
            return grid[x]
        def col(y):
            return [x[y] for x in grid]
        def box(x, y):
            yy = (y//3)*3
            xx = (x//3)*3
            b = []
            for i in range(3):
                for j in range(3):
                    b.append(self.grid[yy+i][xx+j])
            return b

        for x in range(9):
            for y in range(9):
                if self.grid[x][y] != 0:
                    grid[x][y] = str(self.grid[x][y])
                else:
                    p = []
                    for n in range(1,10):
                        if self.possible(x, y, n):
                            p.append(str(n))
                    grid[x][y] = ''.join(p)

        for x in range(9):
            for y in range(9):
                r = row(x)
                c = col(y)
                b = box(x,y)
                for i in r:
                    if isinstance(i, str):
                        if r.count(i) == len(i):
                            if grid[x][y] != i:
                                grid[x][y] = str(grid[x][y]).strip(i)
                            if isinstance(grid[x][y], int):
                                if grid[x][y] > 9:
                                    grid[x][y] = str(grid[x][y])
                for i in c:
                    if isinstance(i, str):
                        if c.count(i) == len(i):
                            if grid[x][y] != i:
                                grid[x][y] = str(grid[x][y]).strip(i)
                            if isinstance(grid[x][y], int):
                                if grid[x][y] > 9:
                                    grid[x][y] = str(grid[x][y])

                for i in b:
                    if isinstance(i, str):
                        if b.count(i) == len(i):
                            if grid[x][y] != i:
                                grid[x][y] = str(grid[x][y]).strip(i)
                            if isinstance(grid[x][y], int):
                                if grid[x][y] > 9:
                                    grid[x][y] = str(grid[x][y])
        for x in range(9):
            for y in range(9):
                if isinstance(grid[x][y], str) and len(grid[x][y]) == 1:
                    self.grid[x][y] = int(grid[x][y])
        return self.grid



    def verify(self):

        sgrid = self.grid
        rows = [sgrid[i:i+1] for i in range(9)]
        cols = [sgrid[:, i:i+1] for i in range(9)]
        boxes = [sgrid[i*3:i*3+3, k*3:k*3+3] for i in range(3) for k in range(3)]
        for x, row in enumerate(rows):
            if len(set(row.reshape(9))) != 9:
                return False
        for x, col in enumerate(cols):
            if len(set(col.reshape(9))) != 9:
                return False
        for x, box in enumerate(boxes):
            if len(set(box.reshape(9))) != 9:
                return False
        return True

def single():
    p = puzzles[0]
    g = Sudoku(p)
    g.solve()
    print(g)

@timeit
def main():
    y = 0
    for x, i in enumerate(puzzles):
        g = Sudoku(i)
        if g.solve():
            y += 1
            print(f"\033[38;2;0;255;0mSolved and verified number {x+1} (Total solved: {y})\033[0m")
        else:
            print(f"\033[38;2;255;0;0mSudoku number {x+1} is still too hard for me. Sorry.\033[0m")

if __name__ == '__main__':
    main()