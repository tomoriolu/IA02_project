"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

# import collections
import random
# import ast
import time
from init_obj import create_grid, state_to_grid2, grid_to_state2, symetry_60, \
    symetry_slash, symetry_backslash
from def_types import Cell, Action, ActionGopher, Player, State, Strategy, Score, Time, Grid

# from collections import defaultdict
# import numpy as np


def pprint(grid: Grid):
    "affichage d'une grid sous forme d'une matrice"
    i: int = 0
    for line in grid:
        for _ in range(0, i):
            print("  ", end="")
        for ele in line:
            print(f" {ele:2d} ", end="")
        i += 1
        print()


def adj_box(grid: Grid, ennemy_cell: list[Cell], limited: bool) -> list[Cell]:
    "retourne les cases adjacentes à la case en paramètre"
    list_cell: list[Cell] = []
    from_row: int
    from_col: int
    n: int
    list_cell_tmp: list[Cell]
    for from_cell in ennemy_cell:

        from_row, from_col = from_cell
        n = len(grid)
        list_cell_tmp = [
            (from_row - 1, from_col),
            (from_row - 1, from_col + 1),
            (from_row, from_col - 1),
            (from_row, from_col + 1),
            (from_row + 1, from_col - 1),
            (from_row + 1, from_col),
        ]
        if limited:
            for row, col in list_cell_tmp:
                if (
                    0 <= row < n
                    and 0 <= col < n
                    and grid[row][col] == 0
                    and (row, col) not in list_cell
                ):
                    list_cell.append((row, col))
        else:
            for row, col in list_cell_tmp:
                if 0 <= row < n and 0 <= col < n and (row, col) not in list_cell:
                    list_cell.append((row, col))
    return list_cell


def adj_box_player(grid: Grid, list_cell: list[Cell], player: Player) -> list[ActionGopher]:
    "retourne les cases jouables par le joueur parmi la liste de cases"
    test: bool = True
    cpt: int = 0
    list_final: list[Cell] = []
    for ele in list_cell:
        play_box: list[Cell] = adj_box(grid, [ele], False)
        for row, col in play_box:
            if grid[row][col] == player and test:
                # list_cell.remove(ele)
                test = False
            if grid[row][col] == 3-player:
                cpt+=1
        if test and cpt==1:
            list_final.append(ele)
        test = True
        cpt = 0
    return list_final


def player_box(grid: Grid, player: Player) -> list[Cell]:
    "retourne la liste des cases possées par le joueur"
    liste: list[Cell] = []
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == player:
                liste.append((i, j))
    return liste


def legals_gopher(state: State, player: Player, n: int) -> list[ActionGopher]:
    "retourne la liste de coups possibles pour le joueur"
    grid: Grid = state_to_grid2(state, n)
    if player == 1:
        cell_player: list[Cell] = player_box(grid, 2)
    else:
        cell_player: list[Cell] = player_box(grid, 1)
    if cell_player:
        list_adj = adj_box(grid, cell_player, True)
        return adj_box_player(grid, list_adj, player)
    liste :list[ActionGopher] = []
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 0:
                liste.append((i,j))
    return liste


def plus_action(state: State, player: Player, n: int) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_gopher(state, player, n)


def final_gopher(state: State, player: Player, n: int) -> bool:
    """test si l'etat est un etat final"""
    return plus_action(state, player, n)


def score_gopher(state: State, n) -> int:
    """renvoi le score d'une grille finale"""
    if plus_action(state, 2, n):
        return 1
    if plus_action(state, 1, n):
        return -1
    return 0


def strategy_joueur(state: State, player: Player, n) -> ActionGopher:
    "stratégie pour un joueur"
    test: bool = False
    grid: Grid = state_to_grid2(state, n)
    action: ActionGopher
    print(f"À vous de jouer, joueur {player}")
    while not test:
        print(f"Voici les coups possibles {legals_gopher(state, player, n)}")
        pprint(grid)
        print("Choix de la case")
        print("Ligne : ", end="")
        l = int(input())
        print("Colonne :", end="")
        c = int(input())
        if (l, c) in legals_gopher(state, player, n):
            action = (l, c)
            test = True
        else:
            print("Ce coup n'est pas possible")
    return action

def strategy_first_legal(state: State, player: Player, n) -> ActionGopher:
    "strategy first legal"
    coups : list[ActionGopher] = legals_gopher(state, player, n)
    print(f"Voici les coups jouables : {coups}")
    choix : ActionGopher = coups[0]
    print(f"Choix du joueur {player} : {choix}")
    return choix

def strategy_random_legal(state: State, player: Player, n) -> ActionGopher:
    "strategy random legal"
    coups : list[ActionGopher] = legals_gopher(state, player, n)
    choix : ActionGopher = random.choice(coups)
    return choix


def play_gopher(state: State, player: Player, action: ActionGopher, n: int) -> State:
    "fonction qui modifie le jeu"
    grid: Grid = state_to_grid2(state, n)
    grid[action[0]][action[1]] = player
    return grid_to_state2(grid, n)


def gopher(
    state: State, strategy_1: Strategy, strategy_2: Strategy, n: int, debug: bool = False
) -> Score:
    "boucle de jeu"
    if not debug:
        state = play_gopher(state, 1, strategy_1(state, 1, n), n)
        player: int = 2
        fin: bool = False
        while not fin:
            # print("---------------------------")
            if player == 1:
                state = play_gopher(state, player, strategy_1(state, player, n), n)
                # pprint(state_to_grid2(state, n))
            if player == 2:
                state = play_gopher(state, player, strategy_2(state, player, n), n)
                # pprint(state_to_grid2(state, n))
            if player == 1:
                player = 2
            else :
                player = 1
            if plus_action(state, player, n):
                fin = True
        result: int = score_gopher(state, n)
        # print("---------------------------")
        if result == 0:
            print("Match nul")
        else:
            print(f"Le vainqueur est le joueur {result}")
        pprint(state_to_grid2(state, n))
        return result
    return result



def evaluation(state: State, player: Player, n: int) -> float:
    "fonction d'évaluation pour l'algorithme negamax"
    return (len(legals_gopher(state, player, n)) - len(legals_gopher(state, 3-player, n))) / n*n
    # division par n*n pour normaliser le résultat afin qu'il soit compris entre -1 et 1 


def memoize_cache(f):
    "fonction de cache"
    cache = {}
    def g(state, player, depth, alpha, beta, n):
        state2 = tuple(state) # permet de rendre le state immutable
        if (state2, player) in cache:
            return cache[(state2, player)]
        result = f(state, player, depth, alpha, beta, n)
        # if result == 0 or result == 1:
        cache[(state2, player)] = result
        return result
    return g


def memoize_cache2(f):
    "fonction de cache avec traitement des symétries"
    cache = {}
    def g(state, player, depth, alpha, beta, n):
        state2 = tuple(state)
        symmetries = [
            state2,
            tuple(symetry_60(state)),
            tuple(symetry_slash(state)),
            tuple(symetry_backslash(state))
        ]
        for sym_state in symmetries:
            if (sym_state, player, depth) in cache:
                return cache[(sym_state, player, depth)]
        result = f(state, player, depth, alpha, beta, n)
        for sym_state in symmetries:
            cache[(sym_state, player, depth)] = result
        return result
    return g


@memoize_cache
def negamax_alpha_beta(state: State, player: Player, depth: int,
    alpha: float, beta: float, n: int) -> tuple[float, Action]:
    "algorithme negamax"
    if depth == 0 or final_gopher(state, player, n):
        if final_gopher(state, player, n):
            if player == 1:
                score = -1
            else:
                score = 1
        else:
            score = evaluation(state, player, n)
        return score, None
    best_score = float('-inf')
    best_action = None
    for action_possible in legals_gopher(state, player, n):
        new_state = play_gopher(state, player, action_possible, n)
        score = - negamax_alpha_beta(new_state, 3 - player, depth - 1, -beta, -alpha, n)[0]
        if score > best_score:
            best_score = score
            best_action = action_possible
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return best_score, best_action

def strategy_negamax_alpha_beta(state: State, player: Player, n: int) -> ActionGopher:
    "stratégie appelant l'algorithme negamax"
    alpha = float('-inf')
    beta = float('inf')
    depth = 7
    _, best_action = negamax_alpha_beta(state, player, depth, alpha, beta, n)
    return best_action




# n = 5
# c = 0
# start_time = time.time()
# for i in range(10):
#     result = gopher(grid_to_state2(create_grid(n), n),
#         strategy_negamax_alpha_beta, strategy_negamax_alpha_beta, n)
#     if result==1:
#         c += 1

# print(f"{c}/100")
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Temps d'exécution : {execution_time} secondes")


# t = create_grid(n)
# p = play_gopher(grid_to_state2(t, n), 1, strategy_negamax_alpha_beta(grid_to_state2(t, n), 1, n), n)
# pprint(state_to_grid2(p, n))
# p = play_gopher(p, 2, strategy_first_legal())