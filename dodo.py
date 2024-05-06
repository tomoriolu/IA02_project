from typing import Callable, List, Dict, Tuple
import random
import ast
import time

Grid = tuple[tuple[int, ...], ...] #tuple non mutable donc peut etre clé d'un dico : utilisé pour coder des jeux
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[State, Player], Action]

def hex_to_tab(i: int, j: int)->Tuple(int,int):
    
def tab_to_hexs(i: int, j: int)->Tuple(int,int):

def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]] :
    
def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid : 


def actions(grid: State) -> Grid: