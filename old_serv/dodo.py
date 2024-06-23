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
# state = []
cells_joueur_2: list[Cell] = []
# def hex_to_tab(i: int, j: int)->Tuple(int,int):

# def tab_to_hexs(i: int, j: int)->Tuple(int,int):

# def actions(grid: State) -> Grid:

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

def pprint(grid):
    "affichage d'une grid sous forme d'une matrice"
    for line in grid:
        for ele in line:
            print(f" {ele:2d} ", end="")
        print()

def set_grid(grid: Grid) -> Grid:
    "initialise un grid pour un début de partie"
    # premier joueur
    n: int = len(grid) // 2
    for i in range(n + 2):
        for j in range(n + i - 1, n * 2 + 1):
            if grid[i][j] != -1:
                grid[i][j] = 1
                # state.append(((i, j), 1))
    # print(state)

    for i in range(n, len(grid)):
        for j in range(0, i - n + 2):
            if grid[i][j] != -1:
                grid[i][j] = 2
                # state.append(((i, j), 2))
    # print(state)
    return grid


# print(set_grid(state_to_grid(grid_to_state(create_grid()))))


def is_valid_move(grid: Grid, to_cell: Cell) -> bool:
    "indique si une case peut être atteinte"
    n: int = len(grid)
    to_row: int
    to_col: int
    to_row, to_col = to_cell
    if 0 <= to_row < n and 0 <= to_col < n and grid[to_row][to_col] == 0:
        return True
    return False


def legals_dodo2(state: State, player: Player) -> list[ActionDodo]:
    "donne les coups possibles à partir d'un état de jeu et du joueur désiré"
    actions: list[ActionDodo] = []
    grid = state_to_grid(state)
    directions = {
        1: [
            ((1, -1), "mouvement en bas a gauche"),
            ((0, -1), "mouvement a gauche"),
            ((1, 0), "mouvement en bas"),
        ],
        2: [
            ((-1, 1), "mouvement en haut à droite"),
            ((0, 1), "mouvement à droite"),
            ((-1, 0), "mouvement en haut"),
        ],
    }
    for cell, joueur in state:
        if player == joueur:
            for (d_row, d_col), _ in directions[player]:
                new_cell = (cell[0] + d_row, cell[1] + d_col)
                if is_valid_move(grid, new_cell):
                    actions.append((cell, new_cell))

    return actions


# pprint(set_grid(create_grid(3)))

# print(is_valid_move(set_grid(create_grid(3)), (2,1), (0,5)))


# def legals_dodo(state: State, player: Player) -> list[ActionDodo]:
#     "donne les coups possibles à partir d'un état de jeu et du joueur désiré"
#     actions: list[ActionDodo] = []
#     # print(state)
#     grid = state_to_grid(state)
#     for cell, joueur in state:
#         if player == 1 and player == joueur:
#             if cell[0] + 1 < len(grid) and cell[1] - 1 >= 0:
#                 if grid[cell[0] + 1][cell[1] - 1] == 0:  # mouvement en bas a gauche
#                     actions.append(((cell[0], cell[1]), (cell[0] + 1, cell[1] - 1)))
#             if cell[1] - 1 >= 0:
#                 if grid[cell[0]][cell[1] - 1] == 0:  # mouvement a gauche
#                     actions.append(((cell[0], cell[1]), (cell[0], cell[1] - 1)))
#             if cell[0] + 1 < len(grid):
#                 if grid[cell[0] + 1][cell[1]] == 0:  # mouvement en bas
#                     actions.append(((cell[0], cell[1]), (cell[0] + 1, cell[1])))
#         elif player == 2 and player == joueur:
#             if cell[1] + 1 < len(grid) and cell[0] - 1 >= 0:
#                 if grid[cell[0] - 1][cell[1] + 1] == 0:  # en haut à droite
#                     actions.append(((cell[0], cell[1]), (cell[0] - 1, cell[1] + 1)))
#             if cell[1] + 1 < len(grid):
#                 if grid[cell[0]][cell[1] + 1] == 0:  # à droite
#                     actions.append(((cell[0], cell[1]), (cell[0], cell[1] + 1)))
#             if cell[0] - 1 < len(grid):
#                 if grid[cell[0] - 1][cell[1]] == 0:  # en haut
#                     actions.append(((cell[0], cell[1]), (cell[0] - 1, cell[1])))
#     # pprint(grid)
#     return actions


def plus_action(state: State, player: Player) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_dodo2(state, player)
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
        if ((l1, c1), (l2, c2)) in legals_dodo2(state, player):
            action = ((l1, c1), (l2, c2))
            test = True
        else:
            print("Ce coup n'est pas possible")
    return action


def strategy_first_legal(state: State, player: Player) -> ActionDodo:
    "stratégie premier coup possible"
    coups: list[ActionDodo] = legals_dodo2(state, player)
    choix: ActionDodo = coups[0]
    print(f"Choix du joueur {player} : {choix}")
    return choix

def strategy_random(state: State, player: Player) -> ActionDodo:
    "stratégie qui joue un coup random"
    coups: list[ActionDodo] = legals_dodo2(state, player)
    choix: ActionDodo = coups[random.randint(0,len(coups)-1)]
    return choix

def memoize2(f: Callable[[State, Player], tuple[Score, Action]]) -> Callable[[State, Player], tuple[Score, list[Action]]]:
    cache = {} # closure
    def g(state: State, player: Player):
        #state_en_grid = state_to_grid(state)
        state_tuple = tuple(map(tuple, state))  # Convertir l'état en tuple
        if  state_tuple in cache:
            return cache[ state_tuple]
        val = f(state, player)
        cache[ state_tuple] = val
        return val
    return g

@memoize2
def minmax_action(grid: State, player: Player) -> tuple[Score, Action]:
    #time.sleep(1)
    #pprint(grid)
    if plus_action(grid,1) or plus_action(grid,2):
        print("bengala")
        return (score_dodo(grid), ((-1, -1),(-1, -1)))
    print("bengala et ma grosse bite")
    if player==1: # maximizing player
        bestScore = float('-inf')
        for action_possible in legals_dodo2(grid, 1):
            #print("Action possible pour joueur 1:", action_possible)
            score_obtenu, _ = minmax_action(play_dodo(grid, 1, action_possible), 2)
            if bestScore<score_obtenu:                
                bestScore = score_obtenu
                bestAction = action_possible
        return bestScore, bestAction    
    else: # minimizing player
        bestScore = float('inf')
        for action_possible in legals_dodo2(grid, 2):
            #print("Action possible pour joueur 2:", action_possible)
            score_obtenu, _ = minmax_action(play_dodo(grid, 2, action_possible), 1)
            if bestScore>score_obtenu:
                bestScore = score_obtenu
                bestAction = action_possible
        return bestScore, bestAction

def strategy_minmax(grid: State, player: Player) -> Action:
    strategy = minmax_action(grid, player)
    return strategy[1]

def eval_coups(state: State) -> int: 
    evalJoueur1 : int = len(legals_dodo2(state, 1))
    evalJoueur2 : int = len(legals_dodo2(state, 2))
    eval = evalJoueur2 - evalJoueur1
    return eval

def alphabeta(grid: State, player: Player, alpha: float = float('-inf'), beta: float =float('inf'), depth: int = 4) -> tuple[Score, Action]:
    if final_dodo(grid) or depth == 0:
        if final_dodo(grid):
            score = score_dodo(grid)
        else:
            score = eval_coups(grid)
        return (score, None)
    if player==1: # maximizing player
        bestValue = float('-inf')
        for child in legals_dodo2(grid, 1):
            v , _ = alphabeta(play_dodo(grid, 1, child), 2, alpha, beta, depth - 1)
            bestValue = max(bestValue, -v)
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                #print("coupure alpha")
                break
        return bestValue, child
    else: # minimizing player
        bestValue = float('inf')
        for child in legals_dodo2(grid,2):
            v, _ = alphabeta(play_dodo(grid, 2, child), 1, alpha, beta, depth - 1)
            bestValue = min(bestValue, v)
            beta = min(beta, bestValue)
            if alpha >= beta:
                #print("coupure beta")
                break
        return bestValue, child

def strategy_alphabeta(grid: State, player: Player) -> Action:
    strategy = alphabeta(grid, player)
    return strategy[1]

def play_dodo(state: State, player: Player, action: ActionDodo) -> State:
    "fonction qui modifie le jeu"
    grid: Grid = state_to_grid(state)
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
            #print("---------------------------")
            #pprint(state_to_grid(state))
            #time.sleep(1)
            if player == 1:
                state = play_dodo(state, player, strategy_1(state, player))
                player = 2
            else:
                state = play_dodo(state, player, strategy_2(state, player))
                player = 1
        result: int = score_dodo(state)
        # print("---------------------------")
        # if result == 0:
        #     print("Match nul")
        # else:
        #     print(f"Le vainqueur est le joueur {result}")
        # pprint(state_to_grid(state))
        return result
    return result



def main() -> None:
    vic_joueur1 = 0
    for i in range(100):
        score = dodo(grid_to_state(set_grid(create_grid(4))), strategy_alphabeta,strategy_random )
        if score == 1:
            vic_joueur1+=1
    
    print(vic_joueur1)
    
    
    
if __name__ == "__main__":
    main()