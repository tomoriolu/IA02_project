"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

import collections
from typing import Callable, Union
import random
import ast
import time
from init_obj import create_grid, state_to_grid, grid_to_state, state_to_grid2, grid_to_state2, \
    state_to_tuple
from collections import defaultdict

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
    for line in grid:
        for ele in line:
            print(f" {ele:2d} ", end="")
        print()

def set_grid(grid: Grid) -> Grid:
    "initialise un grid pour un début de partie"
    n: int = len(grid) // 2
    for i in range(n + 2):
        for j in range(n + i - 1, n * 2 + 1):
            if grid[i][j] != -1:
                grid[i][j] = 2
    for i in range(n, len(grid)):
        for j in range(0, i - n + 2):
            if grid[i][j] != -1:
                grid[i][j] = 1
    return grid




def is_valid_move(grid: Grid, to_cell: Cell) -> bool:
    "indique si une case peut être atteinte"
    n: int = len(grid)
    to_row: int
    to_col: int
    to_row, to_col = to_cell
    if 0 <= to_row < n and 0 <= to_col < n and grid[to_row][to_col] == 0:
        return True
    return False


def legals_dodo2(state: State, player: Player, n: int) -> list[ActionDodo]:
    "donne les coups possibles à partir d'un état de jeu et du joueur désiré"
    actions: list[ActionDodo] = []
    grid = state_to_grid2(state, n)
    directions = {
        2: [
            ((1, -1), "mouvement en bas a gauche"),
            ((0, -1), "mouvement a gauche"),
            ((1, 0), "mouvement en bas"),
        ],
        1: [
            ((-1, 1), "mouvement en haut à droite"),
            ((0, 1), "mouvement à droite"),
            ((-1, 0), "mouvement en haut"),
        ],
    }
    for cell, joueur in state:
        if player == joueur:
            for (d_row, d_col), _ in directions[player]:
                new_cell = (-cell[1]+n-1 + d_row, n-1+cell[0] + d_col)
                if is_valid_move(grid, new_cell):
                    actions.append(((-cell[1]+n-1, n-1+cell[0]), new_cell))
    return actions


def plus_action(state: State, player: Player, n: int) -> bool:
    """test si le joueur n'a plus d'action"""
    return not legals_dodo2(state, player, n)


def final_dodo(state: State, n: int) -> bool:
    """test si l'etat est un etat final"""
    return plus_action(state, 1, n) or plus_action(state, 2, n)


def score_dodo(state: State, n: int) -> int:
    """renvoi le score d'une grille finale"""
    if plus_action(state, 1, n):
        return 1
    if plus_action(state, 2, n):
        return -1
    return 0


def strategy_joueur(state: State, player: Player, n: int) -> ActionDodo:
    "stratégie pour un joueur"
    test: bool = False
    grid: Grid = state_to_grid2(state, n)
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
        if ((l1, c1), (l2, c2)) in legals_dodo2(state, player, n):
            action = ((l1, c1), (l2, c2))
            test = True
        else:
            print("Ce coup n'est pas possible")
    return action


def strategy_first_legal(state: State, player: Player, n: int) -> ActionDodo:
    "stratégie premier coup possible"
    coups: list[ActionDodo] = legals_dodo2(state, player, n)
    choix: ActionDodo = coups[0]
    print(f"Choix du joueur {player} : {choix}")
    return choix

def strategy_random(state: State, player: Player, n: int) -> ActionDodo:
    "stratégie qui joue un coup random"
    coups: list[ActionDodo] = legals_dodo2(state, player, n)
    choix: ActionDodo = coups[random.randint(0,len(coups)-1)]
    # print(f"Choix du joueur {player} : {choix}")
    return choix


def play_dodo(state: State, player: Player, action: ActionDodo, n: int) -> State:
    "fonction qui modifie le jeu"
    grid: Grid = state_to_grid2(state, n)
    grid[action[0][0]][action[0][1]] = 0
    grid[action[1][0]][action[1][1]] = player
    return grid_to_state2(grid, n)

def eval_coups(state: State, n: int) -> int: 
    evalJoueur1 : int = len(legals_dodo2(state, 1, n))
    evalJoueur2 : int = len(legals_dodo2(state, 2, n))
    eval = evalJoueur2 - evalJoueur1
    return eval/n**2 

def eval_coups2(state: State, n: int) -> int: 
    directions = {
        2: [
            ((1, -1), "mouvement en bas a gauche"),
            ((0, -1), "mouvement a gauche"),
            ((1, 0), "mouvement en bas"),
        ],
        1: [
            ((-1, 1), "mouvement en haut à droite"),
            ((0, 1), "mouvement à droite"),
            ((-1, 0), "mouvement en haut"),
        ],
    }
    grid = state_to_grid2(state, n)
    coupsJoueur1 = legals_dodo2(state, 1, n)
    coupsJoueur2 = legals_dodo2(state, 2, n)
    evalJoueur1 : int = len(coupsJoueur1)
    evalJoueur2 : int = len(coupsJoueur2)
    for cell, _ in coupsJoueur1:
        for (d_row, d_col), _ in directions[1]:
            if not is_valid_move(grid, (cell[0] + d_row, cell[1] + d_col) ):
                evalJoueur2+=5
    for cell, _ in coupsJoueur2:
        for (d_row, d_col), _ in directions[2]:
            if not is_valid_move(grid, (cell[0] + d_row, cell[1] + d_col) ):
                evalJoueur1+=5    
    eval = evalJoueur2 - evalJoueur1
    return eval

def dodo(
    state: State, strategy_1: Strategy, strategy_2: Strategy, n: int, debug: bool = False
) -> Score:
    "boucle de jeu"
    if not debug:
        player: int = 1
        fin: bool = False
        while not fin:
            if not plus_action(state, player, n):
                if player == 1:
                    state = play_dodo(state, player, strategy_1(state, player, n), n)
                else:
                    state = play_dodo(state, player, strategy_2(state, player, n), n)
                player = 3 - player
            else:
                fin = True
        result: int = score_dodo(state, n)
        print(f"Le vainqueur est le joueur {result}")
        return result
    return result



def monte_carlo_simulation(state: State, player: Player, n: int, simulations: int) -> ActionDodo:
    "Stratégie de Monte Carlo pour choisir le meilleur mouvement"

    actions = legals_dodo2(state, player, n)
    if not actions:
        return None
    
    action_scores = {action: 0 for action in actions}
    
    for action in actions:
        for _ in range(simulations):
            result_state = play_dodo(state, player, action, n)
            result_player = 3 - player

            while not final_dodo(result_state, n):
                result_state = play_dodo(result_state, result_player, strategy_random(result_state, result_player, n), n)
                result_player = 3 - result_player
            score = score_dodo(result_state, n)
            if player == 1:
                action_scores[action] += score
            else:
                action_scores[action] -= score

    best_action = max(action_scores, key=action_scores.get)
    return best_action

def strategy_monte_carlo(state: State, player: Player, n: int) -> ActionDodo:
    simulations: int = 150
    return monte_carlo_simulation(state, player, n, simulations)



def main() -> None:
    vic_joueur1 = 0
    start_time = time.time()
    n = 4
    for _ in range(20):
        score = dodo(grid_to_state2(set_grid(create_grid(n)), n), strategy_monte_carlo, strategy_random, n)
        if score == 1:
            vic_joueur1+=1
    print(f"{vic_joueur1}/20")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Temps d'exécution : {execution_time} secondes")  
    
    
    
if __name__ == "__main__":
    main()