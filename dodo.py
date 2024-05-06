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

#def hex_to_tab(i: int, j: int)->Tuple(int,int):
    
#def tab_to_hexs(i: int, j: int)->Tuple(int,int):

#def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]] :
    
#def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid : 


#def actions(grid: State) -> Grid:
    
def create_grid(n: int) -> Grid:
    grid: list = []
    for i in range(2*n+1):
        line: list[int] = []
        for j in range(2*n+1):
            line.append(-1)
        grid.append(line)
    distance: int = n
    for i in range(n+1):
        for j in range(distance,2*n+1):
            grid[i][j]=0
        distance-=1
    distance: int = 2*n
    for i in range(n+1,2*n+1):
        for j in range(0,distance):
            grid[i][j]=0
        distance-=1
    return grid

def affichage(grid):
    for i in grid:
        print(i)
            

        
        
    
#def set_grid(grid: Grid) -> Grid:
    
    

affichage(create_grid(3))