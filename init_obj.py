"""
    Partie fonctions d'initialisation des objets 
"""

from typing import Callable, Union
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
# state = []
cells_joueur_2: list[Cell] = []



def create_grid(n: int = 7) -> Grid:
    "fonction qui initialise une grille au format hexagonale"
    grid: list = []
    distance: int
    for i in range(2 * n - 1):
        line: list[int] = []
        for j in range(2 * n - 1):
            line.append(-1)
        grid.append(line)
    distance = n - 1
    for i in range(n):
        for j in range(distance, 2 * n - 1):
            grid[i][j] = 0
        distance -= 1
    distance = 2 * n - 1
    for i in range(n - 1, distance):
        for j in range(0, distance):
            grid[i][j] = 0
        distance -= 1
    return grid


def size_state(state: State) -> int:
    "détermine la taille d'un objet State pour pouvoir passer d'un State à un Grid"
    l = len(state)
    q = math.sqrt(l)
    return int(q // 2 + 1)


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