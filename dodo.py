"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

import collections
from typing import Callable, Union
import random
import ast
import time
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
state = []
cells_joueur_2: list[Cell] = []
# def hex_to_tab(i: int, j: int)->Tuple(int,int):

# def tab_to_hexs(i: int, j: int)->Tuple(int,int):

# def actions(grid: State) -> Grid:

DEFAULT_RETURN = -255
test_state: State = [
    ((1, 5), 1),
    ((0, 7), 1),
    ((0, 8), 1),
    ((0, 9), 1),
    ((0, 10), 1),
    ((0, 11), 1),
    ((0, 12), 1),
    ((1, 6), 1),
    ((1, 7), 1),
    ((1, 8), 1),
    ((1, 9), 1),
    ((1, 10), 1),
    ((1, 11), 1),
    ((1, 12), 1),
    ((2, 7), 1),
    ((2, 8), 1),
    ((2, 9), 1),
    ((2, 10), 1),
    ((2, 11), 1),
    ((2, 12), 1),
    ((3, 8), 1),
    ((3, 9), 1),
    ((3, 10), 1),
    ((3, 11), 1),
    ((3, 12), 1),
    ((4, 9), 1),
    ((4, 10), 1),
    ((4, 11), 1),
    ((4, 12), 1),
    ((5, 10), 1),
    ((5, 11), 1),
    ((5, 12), 1),
    ((6, 11), 1),
    ((6, 12), 1),
    ((6, 0), 2),
    ((6, 1), 2),
    ((7, 0), 2),
    ((7, 1), 2),
    ((7, 2), 2),
    ((8, 0), 2),
    ((8, 1), 2),
    ((8, 2), 2),
    ((8, 3), 2),
    ((9, 0), 2),
    ((9, 1), 2),
    ((9, 2), 2),
    ((9, 3), 2),
    ((9, 4), 2),
    ((10, 0), 2),
    ((10, 1), 2),
    ((10, 2), 2),
    ((10, 3), 2),
    ((10, 4), 2),
    ((10, 5), 2),
    ((11, 0), 2),
    ((11, 1), 2),
    ((11, 2), 2),
    ((11, 3), 2),
    ((11, 4), 2),
    ((11, 5), 2),
    ((11, 6), 2),
    ((12, 0), 2),
    ((12, 1), 2),
    ((12, 2), 2),
    ((12, 3), 2),
    ((12, 4), 2),
    ((12, 5), 2),
    ((12, 6), 2),
]


def create_grid(n: int = 7) -> Grid:
    "fonction qui initialise une grille au format hexagonale"
    grid: list = []
    for i in range(2 * n - 1):
        line: list[int] = []
        for j in range(2 * n - 1):
            line.append(-1)
        grid.append(line)
    distance: int = n - 1
    for i in range(n):
        for j in range(distance, 2 * n - 1):
            grid[i][j] = 0
        distance -= 1
    distance: int = 2 * n - 1
    for i in range(n - 1, distance):
        for j in range(0, distance):
            grid[i][j] = 0
        distance -= 1
    return grid


def pprint(grid):
    "affichage d'une grid sous forme d'une matrice"
    for line in grid:
        for ele in line:
            print(f" {ele:2d} ", end="")
        print()


def size_state(state: State) -> int:
    "détermine la taille d'un objet State pour pouvoir passer d'un State à un Grid"
    l = len(state)
    q = math.sqrt(l)
    return q // 2 + 1


def state_to_grid(state: State) -> Grid:
    "permet de passer d'un objet State à un Grid"
    n: int = int(size_state(state))
    grid: Grid = create_grid(n)
    for cell, player in state:
        # print(cell)
        # print(player)
        grid[(cell[0])][(cell[1])] = player
    return grid


def grid_to_state(grid: Grid) -> State:
    "permet de passer d'un objet Grid à un State"
    state: State = []
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            state.append(((i, j), value))
    return state


def set_state(grid: Grid) -> Grid:
    "initialise un grid pour un début de partie"
    # premier joueur
    n: int = len(grid) // 2
    for i in range(n + 2):
        for j in range(n + i - 1, n * 2 + 1):
            if grid[i][j] != -1:
                grid[i][j] = 1
                state.append(((i, j), 1))
    # print(state)

    for i in range(n, len(grid)):
        for j in range(0, i - n + 2):
            if grid[i][j] != -1:
                grid[i][j] = 2
                state.append(((i, j), 2))
    # print(state)
    return grid


# print(set_state(state_to_grid(grid_to_state(create_grid()))))


def legals_dodo(state: State, player: Player) -> list[ActionDodo]:
    "donne les coups possibles à partir d'un état de jeu et du joueur désiré"
    actions: list[ActionDodo] = []
    # print(state)
    grid = state_to_grid(state)
    for cell, joueur in state:
        if player == 1 and player == joueur:
            if cell[0] + 1 < len(grid) and cell[1] - 1 >= 0:
                if grid[cell[0] + 1][cell[1] - 1] == 0:  # mouvement en bas a gauche
                    actions.append(((cell[0], cell[1]), (cell[0] + 1, cell[1] - 1)))
            if cell[1] - 1 >= 0:
                if grid[cell[0]][cell[1] - 1] == 0:  # mouvement a gauche
                    actions.append(((cell[0], cell[1]), (cell[0], cell[1] - 1)))
            if cell[0] + 1 < len(grid):
                if grid[cell[0] + 1][cell[1]] == 0:  # mouvement en bas
                    actions.append(((cell[0], cell[1]), (cell[0] + 1, cell[1])))
        elif player == 2 and player == joueur:
            if cell[1] + 1 < len(grid) and cell[0] - 1 >= 0:
                if grid[cell[0] - 1][cell[1] + 1] == 0:  # en haut à droite
                    actions.append(((cell[0], cell[1]), (cell[0] - 1, cell[1] + 1)))
            if cell[1] + 1 < len(grid):
                if grid[cell[0]][cell[1] + 1] == 0:  # à droite
                    actions.append(((cell[0], cell[1]), (cell[0], cell[1] + 1)))
            if cell[0] - 1 < len(grid):
                if grid[cell[0] - 1][cell[1]] == 0:  # en haut
                    actions.append(((cell[0], cell[1]), (cell[0] - 1, cell[1])))
    # pprint(grid)
    return actions


def plus_action(state: State, player: Player) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_dodo(state, player)
    # if legals_dodo(state, player) == []:
    #     return True
    # else:
    #     return False


def final_dodo(state: State) -> bool:
    """test si l'etat est un etat final"""
    return plus_action(state, 1) or plus_action(state, 2)
    # if plus_action(state, 1) or plus_action(state, 2):
    #     return True
    # else:
    #     return False


def score_dodo(state: State) -> int:
    """renvoi le score d'une grille finale"""
    if plus_action(state, 1):
        return 1
    if plus_action(state, 2):
        return -1
    return 0
    # if plus_action(state, 1) and plus_action(
    #     state, 2
    # ):  # je sais pas si c'est possible qu'il y ait égalité
    #     return 0
    # if plus_action(state, 1):
    #     return 1
    # if plus_action(state, 2):
    #     return -1


def strategy_joueur(state: State, player: Player) -> ActionDodo:
    "stratégie pour un joueur"
    test: bool = False
    grid: Grid = state_to_grid(state)
    action: ActionDodo
    print(f"À vous de jouer, joueur {player}")
    while not test:
        pprint(grid)
        print("Choix de la boule à déplacer")
        print("Ligne : ", end="")
        l1 = int(input())
        print("Colonne :", end="")
        c1 = int(input())
        print("Choix de la destination")
        print("Ligne : ", end="")
        l2 = int(input())
        print("Colonne :", end="")
        c2 = int(input())
        if ((l1, c1), (l2, c2)) in legals_dodo(state, player):
            action = ((l1, c1), (l2, c2))
            test = True
        print("Ce coup n'est pas possible")
    return action


def play_dodo(state: State, player: Player, action: ActionDodo) -> State:
    "fonction qui modifie le jeu"
    grid = state_to_grid(state)
    grid[action[0][0]][action[0][1]] = 0
    grid[action[1][0]][action[1][1]] = player
    return grid_to_state(grid)


def dodo(
    state: State, strategy_1: Strategy, strategy_2: Strategy, debug: bool = False
) -> Score:
    "boucle de jeu"
    if not debug:
        player: int = 1
        while not final_dodo(state):
            print("---------------------------")
            if player == 1:
                state = play_dodo(state, player, strategy_1(state, player))
                player = 2
            else:
                state = play_dodo(state, player, strategy_2(state, player))
                player = 1
        result: int = score_dodo(state)
        print("---------------------------")
        if result == 0:
            print("Match nul")
        else:
            print(f"Le vainqueur est le joueur {result}")
        pprint(state_to_grid(state))
        return result
    return result


# dodo(grid_to_state(set_state(create_grid(3))), strategy_joueur, strategy_joueur)
