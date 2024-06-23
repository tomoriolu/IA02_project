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
import numpy as np

# Utilisation de collections pour conserver les évaluations précédentes
from collections import deque


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
            player = 3 - player
            if plus_action(state, player, n):
                fin = True
        result: int = score_gopher(state, n)
        # print("---------------------------")
        print(f"Le vainqueur est le joueur {result}")
        # pprint(state_to_grid2(state, n))
        return result
    return result



def evaluation(state: State, n: int) -> float:
    "fonction d'évaluation pour l'algorithme negamax"
    return len(legals_gopher(state, 1, n)) - len(legals_gopher(state, 2, n))
    # division par n*n pour normaliser le résultat afin qu'il soit compris entre -1 et 1 



def cache(f):
    cache = {}
    def g(state, player, depth, max_depth, n):
        state2 = tuple(state) # permet de rendre le state immutable
        if state2 in cache:
            # print(cache[state2])
            return cache[state2]
        result = f(state, player, depth, max_depth, n)
        # if result == 1 or result == -1:
        cache[state2] = result
        return result
    return g


@cache
def count_victories(state: State, player: Player, depth: int, max_depth: int, n: int):
    """
    Compte le nombre de victoires et de défaites pour chaque branche, et la profondeur.
    """
    if depth == 0 or final_gopher(state, player, n):
        if final_gopher(state, player, n):
            if player == 1:
                score = -1
            else:
                score = 1
        else:
            score = evaluation(state, n)
        if score == 1:
            return (1, 0, max_depth - depth) if player == 1 else (0, 1, max_depth - depth)
        elif score == -1:
            return (0, 1, max_depth - depth) if player == 1 else (1, 0, max_depth - depth)
        if score > 0:
            return (0.01, 0, max_depth - depth) if player == 1 else (0, 0.01, max_depth - depth)
        return (0, 0.01, max_depth - depth) if player == 1 else (0.01, 0, max_depth - depth)

    legal_moves = legals_gopher(state, player, n)
    wins, losses, depths = 0, 0, 0
    
    for move in legal_moves:
        new_state = play_gopher(state, player, move, n)
        w, l, d = count_victories(new_state, 3 - player, depth - 1, max_depth, n)
        wins += w
        losses += l
        depths += d
    
    return (wins, losses, depths)


def best_move(state: State, player: Player, n: int, depth: int) -> ActionGopher:
    """
    Retourne le meilleur coup pour le joueur en utilisant le nombre de victoires / défaites et la profondeur.
    """
    best_ratio = float('-inf')
    best_action = None
    best_depth = float('inf')
    legal_moves = legals_gopher(state, player, n)
    
    for move in legal_moves:
        new_state = play_gopher(state, player, move, n)
        wins, losses, total_depth = count_victories(new_state, 3 - player, depth - 1, depth, n)
        total = wins + losses
        ratio = (wins / total) if total > 0 else 0
        avg_depth = total_depth / total if total > 0 else float('inf')
        
        # print(f"Action: {move}, Wins: {wins}, Losses: {losses}, Avg Depth: {avg_depth:.2f}, Ratio: {ratio:.4f}")
        
        if ratio > best_ratio or (ratio == best_ratio and avg_depth < best_depth):
            best_ratio = ratio
            best_action = move
            best_depth = avg_depth
    
    return best_action


def strategy_mcts(state: State, player: Player, n: int) -> ActionGopher:
    depth = 7
    return best_move(state, player, n, depth)


def main():
    n = 4
    c = 0
    start_time = time.time()
    for i in range(10):
        # result = gopher(grid_to_state2(create_grid(n), n),
        #     strategy_negamax_alpha_beta, strategy_random_legal, n)
        result = gopher(grid_to_state2(create_grid(n), n),
            strategy_mcts, strategy_random_legal, n)
        if result==1:
            c += 1

    print(f"{c}/10")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Temps d'exécution : {execution_time} secondes")



if __name__ == "__main__":
    main()