from typing import List


class Cell:
    """
    Represents a cell in a typical normal form game.
    A cell contains an index for identification purposes,
    the strategies selected to pick this cell, and
    the payoffs for each player at this cell.
    """

    def __init__(self, cell_index: int, strategies=None, payoffs=None):
        if payoffs is None:
            payoffs: List[float] = []
        if strategies is None:
            strategies: List[str] = []
        self.strategies = strategies
        self.payoffs = payoffs
        self.index = cell_index

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def add_payoff(self, payoff: float):
        self.payoffs.append(payoff)

    def add_strategy(self, strategy: str):
        self.strategies.append(strategy)

    def __str__(self):
        return f"Cell index {self.index} with payoffs {self.payoffs} and strategies {self.strategies}."

    def __repr__(self):
        return self.__str__()


class Matrix:
    """
    A class to represent the matrix of a normal form game.
    Stores all cells in a list.
    Also contains a list of all players and a 2-d list of all strategies, where each
    individual list is all strategies for a selected player.
    """

    def __init__(self, players: List[str], strategies: List[List[str]]):
        """
        :param players: List of players in the normal form game
        :param strategies: 2-d list of strategies. The index of the strategy list matches the index in the player list.
        i.e. the list a strategies[0] corresponds to the strategies that can be selected by player[0]
        """
        self.players = players
        self.strategies = strategies
        assert len(players) == len(strategies)
        self.all_cells: List[Cell] = []

    def hml_preference_vector_from_cell(self, cell: Cell) -> str:
        """
        :param cell: The cell to convert to a preference vector.
        :return: The preference vector in hml style for a single cell in string format.
        """
        pv_str: str = "{"
        len_prev: int = 0
        for s in self.strategies:
            for k, strat in enumerate(s):
                pv_str += f"#{k + 1 + len_prev}="
                pv_str += "1," if strat in cell.strategies else "0,"
            len_prev += len(s)
        pv_str = pv_str[:-1]
        pv_str += "}"
        return pv_str

    def hml_all_pref_vec(self, cells: List[Cell]) -> str:
        """
        :param cells: an already ordered list of cells sorted by player's preferences
        :return: string representation of all preference vectors for printing to a hml file.
        """
        all_pv_str = "     "
        for i in range(len(cells)):
            all_pv_str += self.hml_preference_vector_from_cell(cells[i])
            all_pv_str += ",\n     " if i != len(cells) - 1 else "\n"
        return all_pv_str

    def add_cell(self, cell: Cell) -> None:
        """
        Add a cell to the list of cells in the matrix.
        :param cell: the cell to add
        """
        if cell not in self.all_cells:
            self.all_cells.append(cell)
