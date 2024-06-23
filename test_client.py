#!/usr/bin/python3

import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR
from def_types import Action, Player, State, Score, Time
from gopher import strategy_negamax_alpha_beta_gopher, strategy_alphabeta_classique_gopher, strategy_negamax_indeterministe_gopher
from dodo import strategy_alphabeta_indeterministe_dodo, strategy_negamax_alpha_beta_dodo, strategy_monte_carlo, strategy_alphabeta_cache_dodo, strategy_alphabeta_classique_dodo
from init_obj import coordo

Environment = Dict[str, Any]
STRAT_GOPHER = strategy_negamax_alpha_beta_gopher
STRAT_DODO = strategy_monte_carlo


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    dico : Dict = {}
    dico["size"] = hex_size
    dico["game"] = game
    if game == GOPHER_STR :
        dico["strat"] = STRAT_GOPHER
    elif game == DODO_STR:
        dico["strat"] = STRAT_DODO
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
    action = coordo(action, n, game)
    print(f"Coup choisi : {action}")
    return (env, action)


def final_result(state: State, score: Score, player: Player):
    print(f"Le joueur {player} a gagné.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
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
