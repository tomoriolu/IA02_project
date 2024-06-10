"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

# import collections
from typing import Callable, Union
import random
import ast
import time
from init_obj import create_grid, state_to_grid, grid_to_state, state_to_grid2, grid_to_state2, symetry_60, symetry_slash, symetry_backslash
from collections import defaultdict
import numpy as np
import math

# Types de base utilisés par l'arbitre
Environment = ...  # Ensemble des données utiles (cache, état de jeu...) pour
# que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = int
Time = int
Strategy = Callable[[State, Player], Action]
Grid = list[list[int]]
cells_joueur_2: list[Cell] = []


def pprint(grid):
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
        if limited == True:
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
    list_final: list[Cell] = []
    for ele in list_cell:
        play_box: list[Cell] = adj_box(grid, [ele], False)
        for row, col in play_box:
            if grid[row][col] == player and test:
                # list_cell.remove(ele)
                test = False
        if test:
            list_final.append(ele)
        test = True
    return list_final


def player_box(grid: Grid, player: Player) -> list[Cell]:
    liste: list[Cell] = []
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == player:
                liste.append((i, j))
    return liste


def legals_gopher(state: State, player: Player, n: int) -> list[ActionGopher]:
    grid: Grid = state_to_grid2(state, n)
    if player == 1:
        cell_player: list[Cell] = player_box(grid, 2)
    else:
        cell_player: list[Cell] = player_box(grid, 1)
    if cell_player:
        list_adj = adj_box(grid, cell_player, True)
        # print(f"legals_gopher : joueur {player} {list_adj}")
        return adj_box_player(grid, list_adj, player)
    else:
        liste :list[ActionGopher] = []
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 0:
                    liste.append((i,j))
        return liste


# t = create_grid(2)
# t[0][2] = 2
# pprint(t)
# print(legals_gopher(grid_to_state(t), 1))


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
    # print(f"Voici les coups jouables : {coups}")
    choix : ActionGopher = random.choice(coups)
    # print(f"Choix aléatoire du joueur {player} : {choix}")
    return choix

def premier_coup(state: State, n) -> ActionGopher:
    test: bool = False
    grid: Grid = state_to_grid2(state, n)
    action: ActionGopher
    print(f"À vous de jouer, joueur 1")
    while not test:
        pprint(grid)
        print("Choix de la case")
        print("Ligne : ", end="")
        l = int(input())
        print("Colonne :", end="")
        c = int(input())
        if l < len(grid) and c < len(grid) and grid[l][c] == 0:
            action = (l, c)
            test = True
        else:
            print("Ce coup n'est pas possible")
    return action



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
        # state = play_gopher(state, 1, premier_coup(state))
        state = play_gopher(state, 1, strategy_1(state, 1, n), n)
        # pprint(state_to_grid(state))
        player: int = 2
        fin: bool = False
        while not fin:
            # print("---------------------------")
            if player == 1:
                state = play_gopher(state, player, strategy_1(state, player, n), n)
                # pprint(state_to_grid(state))
            if player == 2:
                state = play_gopher(state, player, strategy_2(state, player, n), n)
                # pprint(state_to_grid(state))
            if player == 1:
                player = 2
            else :
                player = 1
            if plus_action(state, player, n):
                fin = True
            
        result: int = score_gopher(state, n)
        # print("---------------------------")
        # if result == 0:
        #     print("Match nul")
        # else:
        #     print(f"Le vainqueur est le joueur {result}")
        # pprint(state_to_grid(state))
        return result
    return result

def evaluation(state: State, player: Player, n: int) -> float:
    """Fonction d'évaluation pour estimer la valeur d'un état non terminal."""
    # Exemple simplifié : nombre de pions du joueur moins nombre de pions de l'adversaire
    grid: Grid = state_to_grid2(state, n)
    player_count = sum(row.count(player) for row in grid)
    opponent_count = sum(row.count(3 - player) for row in grid)
    return player_count - opponent_count

def memoize_cache(func):
    cache = {}

    def wrapper(state, player, depth, alpha, beta, n):
        state_key = tuple(state)
        if (state_key, player, depth) in cache:
            return cache[(state_key, player, depth)]

        result = func(state, player, depth, alpha, beta, n)
        cache[(state_key, player, depth)] = result
        return result

    return wrapper


def memoize_cache2(func):
    cache = {}

    def wrapper(state, player, depth, alpha, beta, n):
        state_key = tuple(state)
        symmetries = [
            state_key,
            tuple(symetry_60(state)),
            tuple(symetry_slash(state)),
            tuple(symetry_backslash(state))
        ]

        for sym_state in symmetries:
            if (sym_state, player, depth) in cache:
                return cache[(sym_state, player, depth)]

        result = func(state, player, depth, alpha, beta, n)
        for sym_state in symmetries:
            cache[(sym_state, player, depth)] = result

        return result

    return wrapper


@memoize_cache
def negamax_alpha_beta(state: State, player: Player, depth: int, alpha: float, beta: float, n: int) -> tuple[float, Action]:
    if depth == 0 or final_gopher(state, player, n):
        if final_gopher(state, player, n):
            score = score_gopher(state, n)
        else:
            score = evaluation(state, player, n)
        return score, None
    
    best_score = float('-inf')
    best_action = None
    
    for action_possible in legals_gopher(state, player, n):
        new_state = play_gopher(state, player, action_possible, n)
        score, _ = negamax_alpha_beta(new_state, 3 - player, depth - 1, -beta, -alpha, n)  # 3 - player pour alterner les joueurs
        score = -score  # Négation car c'est le tour de l'adversaire
        if score > best_score:
            best_score = score
            best_action = action_possible
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return best_score, best_action

def strategy_negamax_alpha_beta(state: State, player: Player, n: int) -> ActionGopher:
    alpha=float('-inf')
    beta=float('inf')
    depth=5
    _, best_action = negamax_alpha_beta(state, player, depth, alpha, beta, n)  # Choisissez la profondeur de recherche ici
    return best_action



n = 7
c = 0
# start_time = time.time()
# for i in range(10):
#     result = gopher(grid_to_state2(create_grid(n), n), strategy_negamax_alpha_beta, strategy_random_legal, n)
#     if result==1:
#         c += 1

# print(f"{c}/10")
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Temps d'exécution : {execution_time} secondes")


t = grid_to_state2(create_grid(n), n)
print(strategy_negamax_alpha_beta(t, 1, n))




# tamer = [((-3,3),1), ((1,3), 2), ((0,-6), 1), ((5,6), 2)]

# pprint(state_to_grid2(tamer, 7))
# pprint(state_to_grid2(symetry_60(tamer), 7))
# print(symetry_slash(tamer))