#!/usr/bin/env python

import unittest
import sudoku
import copy

# test puzzle
test = [[0, 7, 0, 6, 4, 0, 0, 0, 2],
        [0, 0, 2, 0, 9, 3, 0, 0, 8],
        [0, 8, 9, 0, 0, 7, 0, 4, 0],
        [2, 0, 0, 3, 0, 0, 8, 7, 5],
        [8, 0, 6, 7, 0, 4, 0, 0, 9],
        [7, 0, 0, 0, 8, 5, 0, 0, 0],
        [0, 0, 7, 8, 0, 1, 6, 0, 4],
        [0, 0, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

test1 = [[4, 6, 2, 0, 0, 8, 3, 1, 0],
        [0, 5, 1, 0, 0, 0, 7, 0, 9],
        [0, 0, 9, 1, 5, 0, 0, 0, 0],
        [0, 2, 8, 0, 4, 0, 0, 7, 0],
        [7, 0, 0, 8, 1, 0, 2, 0, 6],
        [1, 0, 0, 2, 7, 9, 0, 0, 0],
        [2, 0, 5, 6, 3, 4, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 2],
        [0, 0, 4, 0, 0, 7, 1, 0, 0]]

test2 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]

expected = [[1, 7, 3, 6, 4, 8, 5, 9, 2],
        [5, 4, 2, 1, 9, 3, 7, 6, 8],
        [6, 8, 9, 2, 5, 7, 1, 4, 3],
        [2, 9, 4, 3, 1, 6, 8, 7, 5],
        [8, 5, 6, 7, 2, 4, 3, 1, 9],
        [7, 3, 1, 9, 8, 5, 4, 2, 6],
        [9, 2, 7, 8, 3, 1, 6, 5, 4],
        [3, 1, 5, 4, 6, 9, 2, 8, 7],
        [4, 6, 8, 5, 7, 2, 9, 3, 1]]

expected1 = [[4, 6, 2, 7, 9, 8, 3, 1, 5],
        [3, 5, 1, 4, 6, 2, 7, 8, 9],
        [8, 7, 9, 1, 5, 3, 6, 2, 4],
        [5, 2, 8, 3, 4, 6, 9, 7, 1],
        [7, 9, 3, 8, 1, 5, 2, 4, 6],
        [1, 4, 6, 2, 7, 9, 5, 3, 8],
        [2, 1, 5, 6, 3, 4, 8, 9, 7],
        [6, 3, 7, 9, 8, 1, 4, 5, 2],
        [9, 8, 4, 5, 2, 7, 1, 6, 3]]

expected2 = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]]

invalid = [[5, 5, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]]



class TestSudoku(unittest.TestCase):
    def test_is_possible(self):
        self.assertFalse(sudoku.is_possible(test, 4, 3, 7))
        self.assertFalse(sudoku.is_possible(test, 4, 3, 6))
        self.assertTrue(sudoku.is_possible(test, 4, 3, 2))
        self.assertTrue(sudoku.is_possible(test2, 4, 4, 5))
        self.assertFalse(sudoku.is_possible(test2, 4, 4, 3))

    def test_find_empty(self):
        self.assertEqual(sudoku.find_empty(test), (0, 0))
        self.assertEqual(sudoku.find_empty(test1), (0, 3))

    def test_solver(self):
        t = copy.deepcopy(test)
        solutions = []
        sudoku.solve(t, solutions)
        self.assertEqual(len(solutions), 1)
        self.assertListEqual(t, expected)

        t1 = copy.deepcopy(test1)
        solutions1 = []
        sudoku.solve(t1, solutions1)
        self.assertEqual(len(solutions1), 1)
        self.assertListEqual(t1, expected1)

        t2 = copy.deepcopy(test2)
        solutions2 = []
        sudoku.solve(t2, solutions2)
        self.assertEqual(len(solutions2), 1)
        self.assertListEqual(t2, expected2)

    def test_is_valid(self):
        self.assertTrue(sudoku.is_valid_board(expected))
        self.assertTrue(sudoku.is_valid_board(expected1))
        self.assertTrue(sudoku.is_valid_board(expected2))
        self.assertTrue(sudoku.is_solved(expected1))
        self.assertFalse(sudoku.is_solved(test1))
        self.assertFalse(sudoku.is_valid_board(invalid))

    def test_generator(self):
        for i in range(1):
            grid, seed = sudoku.generate()
            solved = copy.deepcopy(grid)
            sudoku.solve(solved)
            self.assertTrue(sudoku.is_valid_board(grid))
            self.assertTrue(sudoku.is_valid_board(solved))
            self.assertTrue(sudoku.is_solved(solved))
            self.assertFalse(sudoku.is_solved(grid))

if __name__ == '__main__':
    unittest.main()
