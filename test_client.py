#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR
from def_types import Cell, Action, ActionDodo, ActionGopher, Player, State, Strategy, Score, Time, Grid
from gopher_v2 import strategy_negamax_alpha_beta
from init_obj import coordo
from time import sleep

Environment = Dict[str, Any]


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    "Initialize the game env"

    if game == GOPHER_STR :
        dico : Dict = {}
        dico["size"] = hex_size
        dico["strat"] = strategy_negamax_alpha_beta
    else:
        print("ratio")


    return dico


def strategy_brain(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    # print(env)
    n: int = env["size"]
    strat: int = env["strat"]
    # sleep(2)
    action = strat(state, player, n)
    print(action)
    action = coordo(action, n)
    # print(state)
    # print(action)

    # print("New state ", state)
    # print("Time remaining ", time_left)
    # print("What's your play ? ", end="")
    # s = input()
    # print()
    # t = ast.literal_eval(s)
    # return (env, t)

    # print("C'EST À MOI")
    # print(action)
    # print(state)

    return (env, action)


def final_result(state: State, score: Score, player: Player):
    if(player == 1):
        print("GAGNÉ !")
    else:
        print("PERDU...")

    # print(f"Ending: {player} wins with a score of {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
    parser.add_argument("-d", "--disable-dodo", action="store_false")
    parser.add_argument("-g", "--disable-gopher", action="store_false")
    args = parser.parse_args()

    available_games = []
    if not args.disable_dodo:
        available_games.append(DODO_STR)
    if not args.disable_gopher:
        available_games.append(GOPHER_STR)

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
