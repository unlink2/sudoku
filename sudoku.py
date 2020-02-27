#!/usr/bin/env python3

import random
import time
import copy
import api

def output(grid):
    for line in grid:
        print(line)
    print('')

def is_possible(grid, y, x, n):
    # check all lines
    for i in range(len(grid[0])):
        if grid[y][i] == n:
            return False
    for i in range(len(grid)):
        if grid[i][x] == n:
            return False

    # check 3x3 cell
    x0 = (x//3) # get center
    y0 = (y//3) # get center
    for i in range(y0*3, y0*3+3):
        for j in range(x0*3, x0*3+3):
            if grid[i][j] == n:
                return False

    return True

def find_empty(grid):
    for y in range(0, 9):
        for x in range(0, 9):
            if grid[y][x] == 0:
                return (y, x)
    return None

# finds a possible solutions
def solve(grid, solutions=None):
    coord = find_empty(grid)
    y = -1
    x = -1
    if not coord:
        if solutions is not None:
            solutions.append(copy.deepcopy(grid))
        return True
    else:
        y, x = coord
    for n in range(1, 10):
        if is_possible(grid, y, x, n):
            grid[y][x] = n
            if solve(grid, solutions):
                return True
            grid[y][x] = 0
    return False

def empty_grid():
    grid = []
    for y in range(0, 9):
        grid.append([])
        for x in range(0, 9):
            grid[y].append(0)
    return grid

# generate a sudoku puzzle
def generate(seed=0, difficulty=40):
    if seed == 0:
        seed = time.time()
    random.seed(seed)
    # returns a 9x9 grid
    grid = empty_grid()

    make_complete_board(grid)

    # make a list of all coordinates
    coordinates = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            coordinates.append((y, x))

    # remove numbers randomly
    # the more we remove the more difficult
    # the puzzle becomes
    # TODO maybe test for uniqueness by checking how many
    # solutions each removed number opens up and if it allows
    # for more than 1 backtrack
    for i in range(0, difficulty):
        # pick coordinate
        n = random.randint(0, len(coordinates)-1)
        y = coordinates[n][0]
        x = coordinates[n][1]
        grid[y][x] = 0
        # remove coordinate from list
        del coordinates[n]

    return grid, seed

# tells if a given board is valid
def is_valid_board(grid):
    for y in range(0, 9):
        for x in range(0, 9):
            n = grid[y][x]
            if n != 0:
                grid[y][x] = 0 # temp set to 0
                if not is_possible(grid, y, x, n):
                    return False
                grid[y][x] = n # reset
    return True

# tells if a board is solved
# correctly
def is_solved(grid):
    for y in range(0, 9):
        for x in range(0, 9):
            n = grid[y][x]
            if n == 0:
                return False
            grid[y][x] = 0 # temp set to 0
            if not is_possible(grid, y, x, n):
                return False
            grid[y][x] = n # reset
    return True

def get_all_empty(grid):
    empty = []
    for y in range(0, 9):
        for x in range(0, 9):
            if grid[y][x] == 0:
                empty.append((y, x))
    return empty

# recursively fill in a board
# retry reduces the amount of empty spaces required to
# break
def make_complete_board(grid):
    # pick cell
    coords = get_all_empty(grid)
    if len(coords) == 0:
        return True

    # pick a random cell
    coord = coords[random.randint(0, len(coords)-1)]
    y = coord[0]
    x = coord[1]
    ns = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(ns)
    n = ns[random.randint(0, len(ns)-1)]


    # fill in and test if solution is valid
    if is_possible(grid, y, x, n):
        grid[y][x] = n
        solved = copy.deepcopy(grid)
        solve(solved)
        if is_solved(solved):
            # fill in next
            return make_complete_board(grid)
        else:
            grid[y][x] = 0
            return make_complete_board(grid)
    return make_complete_board(grid)

if __name__ == '__main__':
    api.run()
