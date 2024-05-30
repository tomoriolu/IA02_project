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
        i+=1
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
            (from_row-1, from_col),
            (from_row-1, from_col+1),
            (from_row, from_col-1),
            (from_row, from_col+1),
            (from_row+1, from_col-1),
            (from_row+1, from_col)
            ]
        if limited==True:
            for row, col in list_cell_tmp:
                if 0 <= row < n and 0 <= col < n and grid[row][col] == 0 and (row, col) not in list_cell:
                    list_cell.append((row, col))
        else:
            for row, col in list_cell_tmp:
                if 0 <= row < n and 0 <= col < n and (row, col) not in list_cell:
                    list_cell.append((row, col))
    return list_cell


def adj_box_player(grid: Grid, list_cell: list[Cell], player: Player):
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


def legals_gopher(state: State, player: Player):
    grid: Grid = state_to_grid(state)
    if player == 1:
        cell_player: list[Cell] = player_box(grid, 2)
    else:
        cell_player: list[Cell] = player_box(grid, 1)
    list_adj = adj_box(grid, cell_player, True)
    # print(f"legals_gopher : joueur {player} {list_adj}")
    return adj_box_player(grid, list_adj, player)


def plus_action(state: State, player: Player) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_gopher(state, player)


def final_gopher(state: State) -> bool:
    """test si l'etat est un etat final"""
    return plus_action(state, 1) or plus_action(state, 2)


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
        state = play_gopher(state, 1, premier_coup(state))
        player: int = 2
        fin: bool = False
        while not fin:
            print("---------------------------")
            if player == 1:
                state = play_gopher(state, player, strategy_1(state, player))
                player = 2
            if plus_action(state, player):
                    fin = True
            if player == 2:
                state = play_gopher(state, player, strategy_2(state, player))
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


gopher(grid_to_state(create_grid(2)), strategy_joueur, strategy_joueur)