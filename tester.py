import random
import math
import time
import copy
import sys
import array as arr
import pandas as pd 
import numpy as np

data = pd.read_csv("cities.csv", usecols=[1,2] ,header=None, skiprows=1)
cities = data.iloc[:15].to_numpy()

def main():
    print(cities)
    cities2 = swap_routes(cities)
    print(cities2)



def inverse(state): ##Working
    "Inverses the order of cities in a route between node one and node two"
    index_j = random.choice(range(len(state)))  #Selects random index
    index_i = random.choice(range(len(state)))  #Finding new index point

    if(index_i == index_j):                     #Checks they are not the same point
        index_i = random.choice(range(len(state)))

    state[min(index_j,index_i):max(index_j,index_i)] = state[min(index_j,index_i):max(index_j,index_i)][::-1]

    return state

def insert(state): ###Works
    "Insert city at node j before node i"
    index_j = random.choice(range(len(state)))  #Selects random index
    index_i = random.choice(range(len(state)))  #Finding new index point

    if(index_i == index_j):                     #Checks they are not the same point
        index_i = random.choice(range(len(state)))
    
    del_state = np.delete(state, index_j ,0)
    state = np.insert(del_state, index_i - 1, state[index_j], 0)    #Repositioning values
    return state

def swap(state):###Works
    "Swaps two random cities with each other"
    pos_one = random.choice(range(len(state)))  #Selects random index
    pos_two = random.choice(range(len(state)))  #Finding new index point
    
    if(pos_two == pos_one):                     #Checks they are not the same point
        pos_two = random.choice(range(len(state)))
    
    state[[pos_one, pos_two]] = state[[pos_two, pos_one]] #Switching values
    return state

def swap_routes(state): #Not Working
    "Select a subroute from a to b and insert it at another position in the route"
    subroute_a = random.choice(range(len(state)))
    subroute_b = random.choice(range(len(state)))

    subroute = state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]
    print(len(subroute))
    print(subroute)
    for i in (0,len(subroute)):
        print(subroute_a + i)
        state = np.delete(state, subroute_a + i,0)
    
    insert_pos = random.choice(range(len(state)))
    for coordinates in subroute:
        print(coordinates)
        state = np.insert(state, insert_pos, coordinates, 0)
    return state

if __name__ == '__main__':
    main()