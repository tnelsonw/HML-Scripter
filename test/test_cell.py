import unittest
from Cell import Cell


class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(1, [], [])  # init empty cell

    def test_add_strategy(self):
        self.assertEqual(len(self.cell.strategies), 0)

        strat: str = "player 1 strat 1"
        self.cell.add_strategy(strat)
        self.assertEqual(len(self.cell.strategies), 1)
        self.assertEqual(strat, self.cell.strategies[0])

        strat2: str = "player 2 strat 1"
        self.cell.add_strategy(strat2)
        self.assertEqual(len(self.cell.strategies), 2)
        self.assertEqual(strat2, self.cell.strategies[1])
        self.assertEqual(self.cell.strategies, [strat, strat2])

    def test_add_payoff(self):
        self.assertEqual(len(self.cell.strategies), 0)

        payoff_val: float = 5
        payoff_val2: float = 3.4

        self.cell.add_payoff(payoff_val)
        self.assertEqual(len(self.cell.payoffs), 1)
        self.assertEqual(payoff_val, self.cell.payoffs[0])

        self.cell.add_payoff(payoff_val2)
        self.assertEqual(len(self.cell.payoffs), 2)
        self.assertEqual(payoff_val2, self.cell.payoffs[1])
        self.assertEqual(self.cell.payoffs, [payoff_val, payoff_val2])

    def test_str(self):
        self.assertEqual("Cell index 1 with payoffs [] and strategies [].", str(self.cell))
        self.cell.add_payoff(5)
        self.cell.add_strategy('strategy')
        self.assertEqual("Cell index 1 with payoffs [5] and strategies ['strategy'].", str(self.cell))

    def test_eq(self):
        cell: Cell = Cell(1, [], [])
        self.assertEqual(self.cell, cell)

    def test_lt(self):
        cell: Cell = Cell(2, [], [])
        self.assertLess(self.cell, cell)


if __name__ == '__main__':
    # system('mypy --disallow-untyped-defs Cell.py')
    unittest.main()
