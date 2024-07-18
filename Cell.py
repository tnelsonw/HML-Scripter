from typing import List


class Cell:

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

    def __init__(self, players: List[str], strategies: List[List[str]]):  #, payoffs: List[List[float]]):  #, indices: List[int]):
        self.players = players
        self.strategies = strategies
        # self.payoffs = payoffs
        # self.indices = indices
        assert len(players) == len(strategies)
        self.all_cells: List[Cell] = []
        # self.all_cells: List[Cell] = [Cell(self.indices[i]) for i in range(len(self.indices))]
        # num_cells: int = 1
        # for s in self.strategies:
        #     num_cells *= len(s)
        #
        # for i in range(len(self.indices)):
        #     self.all_cells.append(Cell(self.indices[i]))

        # self.player_payoffs: List[List[float]] = []  # a list of length (len(self.players)) each containing a list for that corresponding player's payoffs. in same index order as self.indices
        # for i in range(len(players)):
        #     single_player_payoffs: List[float] = [0 for _ in range(len(indices))]
        #     for k in range(len(payoffs)):
        #         index: int = self.indices[k]  # index to put into single player payoffs list
        #         single_player_payoffs[index-1] = self.payoffs[k][i]  # payoff for player i at cell k
        #         # get the cell with the index and append the payoff
        #         c: Cell = [cell for cell in self.all_cells if cell.index == index][0]
        #         c.add_payoff(self.payoffs[k][i])
        #     self.player_payoffs.append(single_player_payoffs)

    # def print_str_strategies_per_player(self, player_name: str) -> str:
    #     """
    #
    #     :return:
    #     """
    #     index: int = self.players.index(player_name)
    #     print_strategies: List[str] = []
    #     len_prev: int = 0
    #     for k, s in enumerate(self.strategies):
    #         print_strategies += [f"{{#{(i+1) + len_prev},{strat}}}" for i, strat in enumerate(s)]
    #         len_prev += len(s)
    #     return ",".join(print_strategies)

    def hml_preference_vector_from_cell(self, cell: Cell) -> str:
        """

        :param cell:
        :return:
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
        :return: string representation for printing to a hml file
        """
        all_pv_str = "     "
        for i in range(len(cells)):
            all_pv_str += self.hml_preference_vector_from_cell(cells[i])
            all_pv_str += ",\n     " if i != len(cells) - 1 else "\n"
        return all_pv_str

    def add_cell(self, cell: Cell):
        if cell not in self.all_cells:
            self.all_cells.append(cell)

