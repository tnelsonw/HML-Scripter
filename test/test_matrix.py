import unittest
from Cell import *


class TestMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix: Matrix = Matrix(['player1', 'player2'], [['player1 strat1', 'player1 strat2'],
                                                              ['player2 strat1', 'player2 strat2']])

    def test_add_cell(self):
        self.assertEqual(len(self.matrix.all_cells), 0)
        self.matrix.add_cell(Cell(1, [], []))
        self.assertEqual(len(self.matrix.all_cells), 1)

    def test_str(self):
        matrix_str: str = f"Matrix with 2 players and 4 total strategies."
        self.assertEqual(matrix_str, str(self.matrix))

    def test_hml_preference_vector_from_cell(self):
        cell: Cell = Cell(4, ['player1 strat2', 'player2 strat2'], [4, 1])
        result_str: str = self.matrix.hml_preference_vector_from_cell(cell)
        test_str: str = '{#1=0,#2=1,#3=0,#4=1}'
        self.assertEqual(test_str, result_str)

    def test_hml_all_pref_vec(self):
        player1_prefs: List[Cell] = [Cell(1, ['player1 strat1', 'player2 strat1'], [1, 4]),
                                     Cell(2, ['player1 strat1', 'player2 strat2'], [2, 3]),
                                     Cell(3, ['player1 strat2', 'player2 strat1'], [3, 2]),
                                     Cell(4, ['player1 strat2', 'player2 strat2'], [4, 1])]
        result_str: str = self.matrix.hml_all_pref_vec(player1_prefs)
        test_str: str = "     {#1=1,#2=0,#3=1,#4=0},\n     {#1=1,#2=0,#3=0,#4=1},\n     {#1=0,#2=1,#3=1,#4=0},\n     {#1=0,#2=1,#3=0,#4=1}\n"
        self.assertEqual(test_str, result_str)


if __name__ == '__main__':
    # system('mypy --disallow-untyped-defs Cell.py')
    unittest.main()
