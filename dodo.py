import collections
from typing import Callable, List, Dict, Tuple, Union
import random
import ast
import time
import math





# Types de base utilisés par l'arbitre
Environment = ... # Ensemble des données utiles (cache, état de jeu...) pour
                  # que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell] # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int # 1 ou 2
State = list[tuple[Cell, Player]] # État du jeu pour la boucle de jeu
Score = int
Time = int
Strategy = Callable[[State, Player], Action]
Grid = list[list[int]]
state = []
cells_joueur_2 : list[Cell] = []
#def hex_to_tab(i: int, j: int)->Tuple(int,int):
    
#def tab_to_hexs(i: int, j: int)->Tuple(int,int):

#def actions(grid: State) -> Grid:
    
def create_grid(n: int = 7) -> Grid:
    grid: list = []
    for i in range(2*n-1):
        line: list[int] = []
        for j in range(2*n-1):
            line.append(-1)
        grid.append(line)
    distance: int = n-1
    for i in range(n):
        for j in range(distance,2*n-1):
            grid[i][j]=0
        distance-=1
    distance: int = 2*n-1
    for i in range(n-1,distance):
        for j in range(0,distance):
            grid[i][j]=0
        distance-=1
    return grid




def pprint(grid):
    for line in grid:
        for ele in line:
            print(f" {ele:2d} ", end="")
        print()

def size_state(state: State) -> int:
    l = len(state)
    q = math.sqrt(l)
    return q // 2 + 1

            
def state_to_grid(state: State) -> Grid:
    n : int = int(size_state(state))
    grid : Grid = create_grid(n)
    for cell, player in state:
        #print(cell)
        #print(player)
        grid[(cell[0])][(cell[1])] = player
    return grid
        
test: State = [((1, 5), 1), ((0, 7), 1), ((0, 8), 1), ((0, 9), 1), ((0, 10), 1), ((0, 11), 1), ((0, 12), 1), ((1, 6), 1), ((1, 7), 1), ((1, 8), 1), ((1, 9), 1), ((1, 10), 1), ((1, 11), 1), ((1, 12), 1), ((2, 7), 1), ((2, 8), 1), ((2, 9), 1), ((2, 10), 1), ((2, 11), 1), ((2, 12), 1), ((3, 8), 1), ((3, 9), 1), ((3, 10), 1), ((3, 11), 1), ((3, 12), 1), ((4, 9), 1), ((4, 10), 1), ((4, 11), 1), ((4, 12), 1), ((5, 10), 1), ((5, 11), 1), ((5, 12), 1), ((6, 11), 1), ((6, 12), 1), ((6, 0), 2), ((6, 1), 2), ((7, 0), 2), ((7, 1), 2), ((7, 2), 2), ((8, 0), 2), ((8, 1), 2), ((8, 2), 2), ((8, 3), 2), ((9, 0), 2), ((9, 1), 2), ((9, 2), 2), ((9, 3), 2), ((9, 4), 2), ((10, 0), 2), ((10, 1), 2), ((10, 2), 2), ((10, 3), 2), ((10, 4), 2), ((10, 5), 2), ((11, 0), 2), ((11, 1), 2), ((11, 2), 2), ((11, 3), 2), ((11, 4), 2), ((11, 5), 2), ((11, 6), 2), ((12, 0), 2), ((12, 1), 2), ((12, 2), 2), ((12, 3), 2), ((12, 4), 2), ((12, 5), 2), ((12, 6), 2)]


def grid_to_state(grid: Grid) -> State:
    state : State = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            state.append(((i, j), grid[i][j]))
    return state

def set_state(grid : Grid) -> Grid:
    #premier joueur
    n: int = len(grid)//2
    for i in range(n+2):
        for j in range(n+i-1, n*2+1):
            if grid[i][j]!=-1:
                grid[i][j] = 1
                state.append(((i,j),1))
    #print(state)
                
    for i in range(n,len(grid)):
        for j in range(0, i-n+2 ):
            if grid[i][j]!=-1:
                grid[i][j] = 2
                state.append(((i,j),2))
    #print(state)
    return(grid)      

# print(set_state(state_to_grid(grid_to_state(create_grid()))))
    
def legals_dodo(state: State, player: Player) -> list[ActionDodo] :
    actions: list[ActionDodo] = []
    #print(state)
    grid = state_to_grid(state)
    for cell, joueur in state:
        if player==1:
            if player==joueur:
                if grid[cell[0] + 1][cell[1] - 1] == 0: #mouvement en bas a gauche
                    actions.append(((cell[0],cell[1]),(cell[0]+1,cell[1]-1)))
                if grid[cell[0]][cell[1]-1]==0: #mouvement a gauche
                    actions.append(((cell[0],cell[1]),(cell[0],cell[1]-1)))
                if grid[cell[0]+1][cell[1]]==0: #mouvement en bas
                    actions.append(((cell[0],cell[1]),(cell[0]+1,cell[1])))
        elif player==2:
            if player==joueur:
                if grid[cell[0]-1][cell[1]+1] == 0: # en haut à droite
                    actions.append(((cell[0], cell[1]), (cell[0]-1, cell[1]+1)))
                if grid[cell[0]][cell[1]+1] == 0: # à droite
                    actions.append(((cell[0], cell[1]), (cell[0], cell[1]+1)))
                if grid[cell[0]-1][cell[1]] == 0: # en haut
                    actions.append(((cell[0], cell[1]), (cell[0]-1, cell[1])))
    pprint(grid)
    return actions


def plus_action(state: State, player: Player ) -> bool:
    """test si le joueur n'a plus d'action"""
    if (legals_dodo(state, player)==[]):
        return True
    else: 
        return False

def final_dodo(state: State) -> bool:
    """test si l'etat est un etat final"""
    if plus_action(state, 1) or plus_action(state, 2):
        return True
    else: 
        return False

def score_dodo():
    """renvoi le score d'une grille finale"""
    if plus_action(state, 1) and plus_action(state, 2): #je sais pas si c'est possible qu'il y ait égalité
        return 0
    if plus_action(state, 1):
        return 1
    if plus_action(state, 2):
        return -1
    


print(legals_dodo(grid_to_state(set_state(state_to_grid(grid_to_state(create_grid(3))))), 1))



# print(grid_to_state(create_grid(3)))
# pprint(state_to_grid(grid_to_state(create_grid(3))))

# print(type(int(size_state(grid_to_state(create_grid(3))))))
    
def jouer_action(state: State, action: Action)-> State:
    print("test")
    
    

#pprint(create_grid(7))
#print()
#pprint(state_to_grid(test))
#set_state(create_grid())
# print(legals_dodo(test,1))

#pprint(set_state(create_grid()))
# print(type(set_state(create_grid())))
#legals_dodo(set_state(create_grid()), 1)

# state_to_grid(set_state(create_grid()))