"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

import collections
from typing import Callable, Union
import random
import ast
import time
from init_obj import create_grid, state_to_grid, grid_to_state


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


def legals_gopher(state: State, player: Player) -> list[ActionGopher]:
    grid: Grid = state_to_grid(state)
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


def plus_action(state: State, player: Player) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_gopher(state, player)


def final_gopher(state: State, player: Player) -> bool:
    """test si l'etat est un etat final"""
    return plus_action(state, player)


def score_gopher(state: State) -> int:
    """renvoi le score d'une grille finale"""
    if plus_action(state, 2):
        return 1
    if plus_action(state, 1):
        return -1
    return 0


def strategy_joueur(state: State, player: Player) -> ActionGopher:
    "stratégie pour un joueur"
    test: bool = False
    grid: Grid = state_to_grid(state)
    action: ActionGopher
    print(f"À vous de jouer, joueur {player}")
    while not test:
        print(f"Voici les coups possibles {legals_gopher(state, player)}")
        pprint(grid)
        print("Choix de la case")
        print("Ligne : ", end="")
        l = int(input())
        print("Colonne :", end="")
        c = int(input())
        if (l, c) in legals_gopher(state, player):
            action = (l, c)
            test = True
        else:
            print("Ce coup n'est pas possible")
    return action

def strategy_first_legal(state: State, player: Player) -> ActionGopher:
    "strategy first legal"
    coups : list[ActionGopher] = legals_gopher(state, player)
    print(f"Voici les coups jouables : {coups}")
    choix : ActionGopher = coups[0]
    print(f"Choix du joueur {player} : {choix}")
    return choix


def premier_coup(state: State) -> ActionGopher:
    test: bool = False
    grid: Grid = state_to_grid(state)
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

# def first_move(state: State) -> ActionGopher:
#     test: bool = False
#     grid: Grid = state_to_grid(state)
#     action: ActionGopher
#     while not test:



def play_gopher(state: State, player: Player, action: ActionGopher) -> State:
    "fonction qui modifie le jeu"
    grid: Grid = state_to_grid(state)
    grid[action[0]][action[1]] = player
    return grid_to_state(grid)


def gopher(
    state: State, strategy_1: Strategy, strategy_2: Strategy, debug: bool = False
) -> Score:
    "boucle de jeu"
    if not debug:
        # state = play_gopher(state, 1, premier_coup(state))
        state = play_gopher(state, 1, strategy_1(state, 1))
        player: int = 2
        fin: bool = False
        while not fin:
            print("---------------------------")
            if player == 1:
                state = play_gopher(state, player, strategy_1(state, player))
                pprint(state_to_grid(state))
                player = 2
            if player == 2:
                state = play_gopher(state, player, strategy_2(state, player))
                pprint(state_to_grid(state))
                player = 1
            if player == 1:
                player = 2
            else :
                player = 1
            if plus_action(state, player):
                fin = True
            
        result: int = score_gopher(state)
        print("---------------------------")
        if result == 0:
            print("Match nul")
        else:
            print(f"Le vainqueur est le joueur {result}")
        pprint(state_to_grid(state))
        return result
    return result

def memoize2(f: Callable[[State, Player], tuple[Score, Action]]) -> Callable[[State, Player], tuple[Score, list[Action]]]:
    cache = {} # closure
    def g(state: State, player: Player):
        immutable_state = tuple(state)  # Convertir la liste d'état en tuple pour le rendre hachable
        if immutable_state in cache:
            return cache[immutable_state]
        val = f(state, player)
        cache[immutable_state] = val
        return val
    return g

@memoize2
def minmax_actions(state: State, player: Player) -> tuple[float, list[Action]]:
    listaction : list[Action] = []
    # print("test")
    if plus_action(state, player):
        # print("zebi ?")
        return (score_gopher(state), [(-1, -1)])
    if player==1: # maximizing player
        bestScore = float('-inf')
        for action_possible in legals_gopher(state, 1):
            score_obtenu, _ = minmax_actions(play_gopher(state, 1, action_possible), 2)
            if bestScore<score_obtenu:
                bestScore = score_obtenu
                listaction = [action_possible]
            if bestScore==score_obtenu:
                listaction.append(action_possible)
    
        return bestScore, listaction
    else: # minimizing player
        bestScore = float('inf')
        for action_possible in legals_gopher(state, 2):
            score_obtenu, _ = minmax_actions(play_gopher(state, 2, action_possible), 1)
            if bestScore>score_obtenu:
                bestScore = score_obtenu
                listaction = [action_possible]
            if bestScore==score_obtenu:
                listaction.append(action_possible)
        return bestScore, listaction
    
def strategy_minmax_random(state: State, player: Player) -> ActionGopher:
    strategy = minmax_actions(state, player)
    listAction = strategy[1]
    taille_list_action = len(listAction)
    return listAction[random.randint(0,taille_list_action-1)]

# pprint(create_grid(3))


# for i in range(0,5):
#     start_time = time.time()
#     gopher(grid_to_state(create_grid(3)), strategy_minmax_random, strategy_first_legal)
#     end_time = time.time()

#     execution_time = end_time - start_time
#     print(f"Temps d'exécution : {execution_time} secondes")

start_time = time.time()
gopher(grid_to_state(create_grid(4)), strategy_minmax_random, strategy_first_legal)
end_time = time.time()

execution_time = end_time - start_time
print(f"Temps d'exécution : {execution_time} secondes")