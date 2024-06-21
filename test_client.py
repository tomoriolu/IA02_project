#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR
from def_types import Cell, Action, ActionDodo, ActionGopher, Player, State, Strategy, Score, Time, Grid
from gopher_v2 import strategy_negamax_alpha_beta, strategy_negamax_indeterministe
from dodo_v2 import strategy_alphabeta_indeterministe_dodo, strategy_negamax_alpha_beta_dodo
from gopher_test import strategy_mcts
from init_obj import coordo
from time import sleep

Environment = Dict[str, Any]


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    "Initialize the game env"
    dico : Dict = {}
    dico["size"] = hex_size
    dico["game"] = game
    if game == GOPHER_STR :
        dico["strat"] = strategy_negamax_alpha_beta
    elif game == DODO_STR:
        dico["strat"] = strategy_negamax_alpha_beta_dodo
    print(f"Vous êtes le joueur {player}")
    print(f"Temps total : {total_time}")
    return dico


def strategy_brain(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print(f"Temps restant : {time_left}")
    n: int = env["size"]
    strat = env["strat"]
    game = env["game"]
    action = strat(state, player, n)
    print(f"Coup choisi : {action}")
    action = coordo(action, n, game)

    return (env, action)


def final_result(state: State, score: Score, player: Player):
    print(f"Le joueur {player} a gagné.")

    # print(f"Ending: {player} wins with a score of {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize,
        strategy_brain,
        final_result,
        gui=True,
    )
