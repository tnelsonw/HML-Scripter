import unittest
from typing import List
from hml_scripter import *
from pygambit import Game
from Cell import *


class TestHMLScripter(unittest.TestCase):

    def test_make_pref_vecs(self):
        game: Game = Game.read_game('test_game.gbt')
        matrix: Matrix = Matrix(['player1', 'player2'], [['strat1', 'strat2'], ['strat3', 'strat4']])
        cell1: Cell = Cell(1, ['strat1', 'strat3'], [1, 4])
        cell2: Cell = Cell(2, ['strat1', 'strat4'], [2, 3])
        cell3: Cell = Cell(3, ['strat2', 'strat3'], [3, 2])
        cell4: Cell = Cell(4, ['strat2', 'strat4'], [4, 1])
        matrix.add_cell(cell1)
        matrix.add_cell(cell2)
        matrix.add_cell(cell3)
        matrix.add_cell(cell4)

        func_results: List[List[Cell]] = make_pref_vecs(game, matrix, True)
        test_results: List[List[Cell]] = [[cell4, cell3, cell2, cell1], [cell1, cell2, cell3, cell4]]
        self.assertEqual(test_results, func_results)

        func_results_min: List[List[Cell]] = make_pref_vecs(game, matrix, False)
        test_results_min: List[List[Cell]] = [[cell1, cell2, cell3, cell4], [cell4, cell3, cell2, cell1]]
        self.assertEqual(test_results_min, func_results_min)

    def test_str_hml_strategies(self):
        player_to_strats: dict[str: List[str]] = {'player1': ['strat1', 'strat2'], 'player2': ['strat3', 'strat4']}

        player1_test_str: str = str_hml_strategies(player_to_strats['player1'], 0)
        player1_result_str: str = "{#1,strat1},{#2,strat2}"
        self.assertEqual(player1_test_str, player1_result_str)

        player2_test_str: str = str_hml_strategies(player_to_strats['player2'], len(player_to_strats['player1']))
        player2_result_str: str = "{#3,strat3},{#4,strat4}"
        self.assertEqual(player2_test_str, player2_result_str)


if __name__ == "__main__":
    # system('mypy --disallow-untyped-defs hml_scripter.py')
    unittest.main()