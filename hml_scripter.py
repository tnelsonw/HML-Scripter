from typing import List
from Cell import Cell, Matrix
import pygambit


class GameFormatException(Exception):
    """
    Raise this exception if the game file is not formatted properly.
    """
    pass


def make_pref_vecs(game: pygambit.Game, matrix: Matrix, by_max_val: bool = True) -> List[List[Cell]]:
    """
    Takes the game object, and orders all cells in the matrix by the preferences of each player.
    :param game: the pygambit game object
    :param matrix: the matrix object
    :param by_max_val: a boolean that if true says the game is ordered by maximum preference vectors, where the max
    value is the most preferred preference vector. If false, then the minimum value is the most preferred vector
    :return: a 2-d list of Cells where each list corresponds to each player, i.e. list[0] corresponds to the first
    player's preference vectors, list[1] to the second player's, and so forth.
    """

    all_payoff_vals: List[List[float]] = [[0 for _ in range(len(game.players))] for _ in range(len(game.contingencies))]
    all_strat_vals: List[List[str]] = [["" for _ in range(len(game.players))] for _ in range(len(game.contingencies))]
    all_pref_vecs: List[List[Cell]] = []

    for i, player in enumerate(game.players):
        for k, profile in enumerate(game.contingencies):
            all_payoff_vals[k][i] = game[profile][player.label].numerator
            all_strat_vals[k][i] = player.strategies[profile[i]].label

    for i in range(len(game.contingencies)):
        matrix.add_cell(Cell(i+1, all_strat_vals[i], all_payoff_vals[i]))

    for i, player in enumerate(game.players):
        all_pref_vecs.append(sorted(matrix.all_cells, key=lambda x: x.payoffs[i], reverse=by_max_val))

    return all_pref_vecs


def str_hml_strategies(strats: List[str], printed_so_far: int = 0) -> str:
    """
    :param strats: The list of strategies to print to hml format.
    :param printed_so_far: The number of strategies printed so far.
    :return: A string representation of a player's strategies in hml format.
    """
    print_strategies: List[str] = []
    for k, s in enumerate(strats):
        print_strategies.append(f"{{#{(k+1+printed_so_far)},{s}}}")
    return ",".join(print_strategies)


def main():
    print("Welcome to the Hypergame Markup Language (HML) scripter. This script takes provided information and creates"
          " an HML file to be read into the \nHypergame Analysis Tool (HYPANT) found at "
          "https://users.monash.edu/~lbrumley/hyper.html.\n")

    output_file_name: str = input("Please input the output hml file name to include the .hml extension: ").strip()
    assert output_file_name.endswith(".hml")
    print('\n')

    level: str = ""
    while not level.isdigit():
        level = input("Please input the hypergame level in digit format (3 for 3rd level hypergame, 2 for 2nd level, "
                      "etc.: ").strip()
        # does not check for negative numbers
    hypergame_level: int = int(level)
    print('\n')

    num_players: str = ""
    while not num_players.isdigit():
        num_players = input("Please input the number of players in this hypergame: ").strip()
        # does not check for negative numbers

    print('\n')

    ###
    # all_games: str = ""
    # while len(all_games.split(',')) < 1:
    #     all_games = input("Please input all .nfg or .gbt games that will be used as part of this hypergame.\n"
    #                       "Comma separate them (e.g. game.gbt,game2.gbt,game3.gbt): ").strip()
    # 
    # games_dict: dict[str: pygambit.Game] = {}
    # for game_str in all_games.split(','):
    #     try:
    #         games_dict[game_str] = pygambit.Game.read_game(game_str)
    #     except (ValueError, IOError):
    #         raise GameFormatException(f"Game {game_str} is not properly formatted for pygambit to read.")

    ###

    with open(output_file_name, "w") as output_file_stream:
        output_file_stream.write("{\n")
        num_games_required: int = int(num_players) ** hypergame_level
        # input each game
        for game_num in range(num_games_required):  # number of individual games is 2^level
            output_file_stream.write(" {\n")

            print("\n-------------------------------------------\n")
            perception: str = "," if hypergame_level == 1 else ""
            while len(perception.split(',')) != hypergame_level:
                perception = input("Input the perception of this game, with each perception separated by a comma. The "
                                   "number of perceptions should equal the hypergame level. (i.e, Player 1's perception"
                                   "\nof player 2's perception of player 2's game for a 3rd level hypergame would be "
                                   "'Player 2,Player 2,Player 1'): ").strip()
            print('\n')
            output_file_stream.write("  {" + perception + "},\n")
            output_file_stream.write("  {\n")  # two spaces then curly bracket

            game_file: str = input(f"Input the .nfg or .gbt Gambit game file in the current directory that represents "
                                   f"this perception: ").strip()
            by_max_str: str = input("In this game, is the most preferred preference vector represented by the lowest "
                                    "value or the highest value? (write 'max' or 'min'): ")
            while by_max_str.lower() != "min" and by_max_str.lower() != "max":
                by_max_str = input("Please write 'max' or 'min': ")
            if by_max_str.lower() == "max":
                by_max_bool = True
            if by_max_str.lower() == "min":
                by_max_bool = False

            try:
                game: pygambit.Game = pygambit.Game.read_game(game_file)
            except (ValueError, IOError):
                raise GameFormatException("The game is not properly formatted for pygambit to read.")
            players: List[str] = [p.label for p in game.players]
            all_strategies: List[List[str]] = [[s.label for s in p.strategies] for p in game.players]

            # make matrix
            matrix = Matrix(players, all_strategies)
            game_pref_vecs: List[List[Cell]] = make_pref_vecs(game, matrix, by_max_bool)

            comment: str = input("Please add a comment or description for this game: ").strip().replace('\n', ' ')
            output_file_stream.write(f"   %%{comment}\n")  # 3 spaces then comment

            num_strategies_printed: int = 0
            for i, player in enumerate(players):  # for each player in the game
                output_file_stream.write("   {\n")  # 3 spaces then curly bracket

                current_player_strategies: List[str] = [s.label for s in list(list(game.players)[i].strategies)]

                output_file_stream.write(f"    {player},")
                output_file_stream.write("{")  # curly bracket that wraps all strategies

                print(f"These are player {player}'s strategies:")

                output_file_stream.write(str_hml_strategies(current_player_strategies, num_strategies_printed))
                num_strategies_printed += len(current_player_strategies)

                output_file_stream.write("},")  # curly bracket that wraps all strategies
                # print player name, print strategies

                print("Mutually exclusive options are strategies that cannot be taken simultaneously. In hml files"
                      "they take the form {#1, #2} if strategy #1 and strategy #2 \ncannot be taken simultaneously."
                      "If the preference vectors are done right, adding this in could be optional. When inputting, the"
                      " mutually exclusive \noptions must be comma separated.")

                num_mutex_options: str = ""
                while not num_mutex_options.isdigit():
                    num_mutex_options = input(f"Input the number of mutually exclusive options for "
                                              f"player {player} (0 options is fine): ")

                output_file_stream.write("{")

                mutex_options: List[str] = []
                for h in range(int(num_mutex_options)):
                    mutex_option = (
                        input("Input a mutually exclusive option in the form #1,#4 (if strategy 1 and 4 cannot "
                              "be taken simultaneously): "))
                    mutex_options.append(mutex_option)
                    output_file_stream.write("{" + f"{mutex_option}" + "}")
                    if h != int(num_mutex_options) - 1:
                        output_file_stream.write(",")

                output_file_stream.write("},\n")

                output_file_stream.write("    {\n")  # four spaces, then begin bracket for preference vectors
                output_file_stream.write(matrix.hml_all_pref_vec(game_pref_vecs[i]))
                output_file_stream.write("    }\n")  # four spaces, ending curly bracket for preference vectors

                # output to end the current player
                output_file_stream.write("   }")  # 3 spaces, ending curly bracket for player
                if i != len(players) - 1:
                    output_file_stream.write(",\n")
                else:
                    output_file_stream.write("\n")

            output_file_stream.write("  }\n")

            # end this game output
            if game_num == num_games_required - 1:
                output_file_stream.write(" }\n")
            else:
                output_file_stream.write(" },\n")

        # end file/last closing bracket
        output_file_stream.write("}\n")


if __name__ == "__main__":
    main()
