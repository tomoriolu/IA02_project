"""
    Partie Dodo du projet de IA02 P24 avec augustin le malin et juju la regu
"""

import collections
from typing import Callable, Union
import random
import ast
import time
from init_obj import create_grid, state_to_grid, grid_to_state, state_to_tuple


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
                grid[i][j] = 2
                # state.append(((i, j), 1))
    # print(state)

    for i in range(n, len(grid)):
        for j in range(0, i - n + 2):
            if grid[i][j] != -1:
                grid[i][j] = 1
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


def legals_dodo2(state: State, player: Player, n: int) -> list[ActionDodo]:
    "donne les coups possibles à partir d'un état de jeu et du joueur désiré"
    actions: list[ActionDodo] = []
    grid = state_to_grid(state, n)
    directions = {
        2: [
            (1, -1),  # mouvement en bas à gauche
            (0, -1),  # mouvement à gauche
            (1, 0),  # mouvement en bas
        ],
        1: [
            (-1, 1),  # mouvement en haut à droite
            (0, 1),  # mouvement à droite
            (-1, 0),  # mouvement en haut
        ],
    }
    for cell, joueur in state:
        if player == joueur:
            for d_row, d_col in directions[player]:
                new_cell = (-cell[1] + n - 1 + d_row, n - 1 + cell[0] + d_col)
                if is_valid_move(grid, new_cell):
                    actions.append(((-cell[1] + n - 1, n - 1 + cell[0]), new_cell))
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


def play_dodo(state: State, player: Player, action: ActionDodo, n: int) -> State:
    "fonction qui modifie le jeu"
    grid: Grid = state_to_grid(state, n)
    grid[action[0][0]][action[0][1]] = 0
    grid[action[1][0]][action[1][1]] = player
    return grid_to_state(grid, n)


def dodo(
    state: State,
    strategy_1: Strategy,
    strategy_2: Strategy,
    n: int,
    debug: bool = False,
) -> Score:
    "boucle de jeu"
    if not debug:
        player: int = 1
        fin: bool = False
        while not fin:
            # print("---------------------------")
            # pprint(state_to_grid(state))
            # time.sleep(1)
            if not plus_action(state, player, n):
                if player == 1:
                    state = play_dodo(state, player, strategy_1(state, player, n), n)
                else:
                    state = play_dodo(state, player, strategy_2(state, player, n), n)
                player = 3 - player
            else:
                fin = True

        result: int = score_dodo(state, n)
        # print("---------------------------")
        # if result == 0:
        #     print("Match nul")
        # else:
        print(f"Le vainqueur est le joueur {result}")
        # pprint(state_to_grid(state, n))
        return result
    return result


def strategy_joueur(state: State, player: Player, n: int) -> ActionDodo:
    "stratégie pour un joueur"
    test: bool = False
    grid: Grid = state_to_grid(state, n)
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
    choix: ActionDodo = coups[random.randint(0, len(coups) - 1)]
    # print(f"Choix du joueur {player} : {choix}")
    return choix


def eval_coups(
    state: State,
    n: int,
    p: Player,
) -> int:
    evalJoueur1: int = len(legals_dodo2(state, 1, n))
    evalJoueur2: int = len(legals_dodo2(state, 2, n))
    eval = evalJoueur2 - evalJoueur1
    return eval


def eval_coups2(state: State, n: int, p: Player) -> int:
    if not final_dodo(state, n):
        directions = {
            2: [
                (1, -1),  # mouvement en bas à gauche
                (0, -1),  # mouvement à gauche
                (1, 0),  # mouvement en bas
            ],
            1: [
                (-1, 1),  # mouvement en haut à droite
                (0, 1),  # mouvement à droite
                (-1, 0),  # mouvement en haut
            ],
        }
        grid = state_to_grid(state, n)
        coupsJActuel = legals_dodo2(state, p, n)
        coupsAdversaire = legals_dodo2(state, 3 - p, n)
        evalJActuel: int = len(coupsJActuel)
        evalJAdverse: int = len(coupsAdversaire)
        for cell, _ in coupsJActuel:
            for d_row, d_col in directions[3 - p]:
                if not is_valid_move(grid, (cell[0] + d_row, cell[1] + d_col)):
                    evalJAdverse -= 3
        for cell, _ in coupsAdversaire:
            for d_row, d_col in directions[p]:
                if not is_valid_move(grid, (cell[0] + d_row, cell[1] + d_col)):
                    evalJActuel -= 3
        eval = -(evalJAdverse - evalJActuel)
    else:
        if score_dodo(state, n) > 0:
            eval = 10000
        else:
            eval = -10000
    return eval


def eval_coups3(state: State, n: int, p: Player) -> int:
    if final_dodo(state, n) and p == 1:
        return 10000 if score_dodo(state, n) > 0 else -10000
    if final_dodo(state, n) and p == 2:
        return -10000 if score_dodo(state, n) > 0 else 10000
    directions = {
        2: [
            (1, -1),  # mouvement en bas à gauche
            (0, -1),  # mouvement à gauche
            (1, 0),  # mouvement en bas
        ],
        1: [
            (-1, 1),  # mouvement en haut à droite
            (0, 1),  # mouvement à droite
            (-1, 0),  # mouvement en haut
        ],
    }

    grid = state_to_grid(state, n)
    coupsJActuel = legals_dodo2(state, p, n)
    coupsAdversaire = legals_dodo2(state, 3 - p, n)
    evalJActuel = len(coupsJActuel)
    evalJAdverse = len(coupsAdversaire)
    for action in coupsJActuel:
        _, to_cell = action
        for d_row, d_col in directions[3 - p]:
            new_row, new_col = to_cell[0] + d_row, to_cell[1] + d_col
            if not is_valid_move(grid, (new_row, new_col)):
                evalJAdverse -= 1

    for action in coupsAdversaire:
        _, to_cell = action
        for d_row, d_col in directions[p]:
            new_row, new_col = to_cell[0] + d_row, to_cell[1] + d_col
            if not is_valid_move(grid, (new_row, new_col)):
                evalJActuel -= 1
    if p == 2:
        return evalJActuel - evalJAdverse
    else:
        return -(evalJActuel - evalJAdverse)


def alphabeta_classique(
    grid: State,
    player: Player,
    n: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    depth: int = 4,
) -> tuple[Score, Action]:
    if depth == 0 or plus_action(grid, player, n):
        score = eval_coups(grid, n)
        return score, None

    if player == 1:  # maximizing player
        bestValue = float("-inf")
        for child in legals_dodo2(grid, 1, n):
            v, _ = alphabeta_classique(
                play_dodo(grid, 1, child, n), 2, n, alpha, beta, depth - 1
            )
            bestValue = max(bestValue, -v)
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                # print("coupure alpha")
                break
        return bestValue, child
    else:  # minimizing player
        bestValue = float("inf")
        for child in legals_dodo2(grid, 2, n):
            v, _ = alphabeta_classique(
                play_dodo(grid, 2, child, n), 1, n, alpha, beta, depth - 1
            )
            bestValue = min(bestValue, v)
            beta = min(beta, bestValue)
            if alpha >= beta:
                # print("coupure beta")
                break
        return bestValue, child


def strategy_alphabeta_classique(grid: State, player: Player, n: int) -> Action:
    depth: int = 2
    alpha: float = float("-inf")
    beta: float = float("inf")
    strategy = alphabeta_classique(grid, player, n, alpha, beta, depth)
    return strategy[1]


def alphabeta_cache(
    state: State,
    player: Player,
    n: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    depth: int = 4,
) -> tuple[Score, Action]:
    if depth == 0 or plus_action(state, player, n):
        score = eval_coups2(state, n, player)
        return score, None

    if player == 1:  # maximizing player
        bestValue = float("-inf")
        for child in legals_dodo2(state, 1, n):
            v, _ = alphabeta_cache(
                play_dodo(state, 1, child, n), 2, n, alpha, beta, depth - 1
            )
            bestValue = max(bestValue, -v)
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                # print("coupure alpha")
                break
        return bestValue, child
    else:  # minimizing player
        bestValue = float("inf")
        for child in legals_dodo2(state, 2, n):
            v, _ = alphabeta_cache(
                play_dodo(state, 2, child, n), 1, n, alpha, beta, depth - 1
            )
            bestValue = min(bestValue, v)
            beta = min(beta, bestValue)
            if alpha >= beta:
                # print("coupure beta")
                break
        return bestValue, child


def strategy_alphabeta_cache(grid: State, player: Player, n: int) -> Action:
    depth: int = 3
    alpha: float = float("-inf")
    beta: float = float("inf")
    strategy = alphabeta_cache(grid, player, n, alpha, beta, depth)
    return strategy[1]


def memoize_cachealphabeta(f):
    cache = {}

    def g(state, player, depth, alpha, beta, n):
        state_key: tuple = (tuple(state), alpha, beta)
        if state_key in cache:
            return cache[state_key]
        result = f(state, player, depth, alpha, beta, n)
        if result[1] != None:
            cache[state_key] = result
        return result

    return g


@memoize_cachealphabeta
def alphabeta_indeterministe(
    state: State,
    player: Player,
    n: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    depth: int = 4,
) -> tuple[Score, Action]:
    if depth == 0 or plus_action(state, player, n):
        score = eval_coups(state, n, player)
        return score, None
    best_actions = []
    if player == 1:  # maximizing player
        bestValue = float("-inf")
        for child in legals_dodo2(state, 1, n):
            v, _ = alphabeta_indeterministe(
                play_dodo(state, 1, child, n), 2, n, alpha, beta, depth - 1
            )
            if v > bestValue:
                bestValue = v
                best_actions = [child]
            elif v == bestValue:
                best_actions.append(child)
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break
        return bestValue, random.choice(best_actions)

    else:  # minimizing player
        bestValue = float("inf")
        for child in legals_dodo2(state, 2, n):
            v, _ = alphabeta_indeterministe(
                play_dodo(state, 2, child, n), 1, n, alpha, beta, depth - 1
            )
            if v < bestValue:
                bestValue = v
                best_actions = [child]
            elif v == bestValue:
                best_actions.append(child)
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
        return bestValue, random.choice(best_actions)


def strategy_alphabeta_indeterministe_dodo(
    state: State, player: Player, n: int
) -> Action:
    depth: int = 3
    alpha: float = float("-inf")
    beta: float = float("inf")
    strategy = alphabeta_indeterministe(state, player, n, alpha, beta, depth)
    return strategy[1]


def memoize_cache(f):
    cache = {}

    def g(state, player, depth, alpha, beta, n):
        state_key: tuple = (tuple(state), alpha, beta)
        if state_key in cache:
            return cache[state_key]

        result = f(state, player, depth, alpha, beta, n)
        if result[1] != None:
            cache[state_key] = result
        return result

    return g


@memoize_cache
def negamax_alpha_beta(
    state: State, player: Player, depth: int, alpha: float, beta: float, n: int
) -> tuple[float, Action]:
    if depth == 0 or plus_action(state, player, n):
        score = eval_coups2(state, n)
        return -score, None

    best_score = float("-inf")
    best_action = None

    for action_possible in legals_dodo2(state, player, n):
        new_state = play_dodo(state, player, action_possible, n)
        score = -negamax_alpha_beta(new_state, 3 - player, depth - 1, -beta, -alpha, n)[
            0
        ]
        score = -score

        if score > best_score:
            best_score = score
            best_action = action_possible

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_score, best_action


def strategy_negamax_alpha_beta_dodo(
    state: State, player: Player, n: int
) -> ActionDodo:
    alpha = float("-inf")
    beta = float("inf")
    depth = 6
    _, best_action = negamax_alpha_beta(state, player, depth, alpha, beta, n)
    return best_action


def main() -> None:
    vic_joueur1 = 0
    start_time = time.time()
    n = 4
    for _ in range(100):
        # score = dodo(grid_to_state2(set_grid(create_grid(n)), n), strategy_negamax_alpha_beta_dodo, strategy_random,n)
        score = dodo(
            grid_to_state(set_grid(create_grid(n)), n),
            strategy_random,
            strategy_alphabeta_indeterministe_dodo,
            n,
        )
        if score == 1:
            vic_joueur1 += 1
    print(f"{vic_joueur1}/100")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Temps d'exécution : {execution_time} secondes")

    # t = grid_to_state2(set_grid(create_grid(n)), n)
    # pprint(set_grid(create_grid(n)))
    # print(strategy_negamax_alpha_beta(t, 1, n))

    # n = 4
    # t = grid_to_state(set_grid(create_grid(n)), n)
    # # print(legals_dodo2(t, 1, n))
    # for i in range(9):
    #     t = play_dodo(t, 1, strategy_random(t, 1, n), n)
    #     print(t)
    #     i = strategy_alphabeta_indeterministe_dodo(t, 2, n)
    #     # print(i)
    #     t = play_dodo(t, 2, i, n)
    #     print(t)


if __name__ == "__main__":
    main()
