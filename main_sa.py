import random
import math
import time
import copy
import sys
import pandas as pd 
import numpy as np

data = pd.read_csv("cities.csv", usecols=[1,2] ,header=None, skiprows=1)
best_route = data.iloc[:5000].to_numpy()

best_dis = sys.maxsize
iterations = 2

print(best_route)
def main():
    global best_dis
    global best_route
    global iterations
    convergence_time = 0
    for i in range(0, iterations):     
        i =  i + 1
        print("Iteration Number: " + str(i))
        start = time.time()

        route, route_distance = annealing(best_route)

        print(route)
        if(route_distance < best_dis):
            best_dis = route_distance
            best_route = route 

        time_elapsed = time.time() - start
        convergence_time = convergence_time + time_elapsed
        print(time_elapsed)


    route, route_distance = finishing_annealing(best_route)
    print(route)
    if(route_distance < best_dis):
         best_dis = route_distance
         best_route = route 

    print(best_dis)
    print(best_route)
    print(convergence_time)

def annealing(initial_cities):
    """Peforms simulated annealing to find a solution"""
    best_routedis = 0
    best_route = np.empty((5000, 2))
   
    initial_temp = 10000
    alpha = 0.99
    
    current_temp = initial_temp

    # Start by initializing the current list with the initial list
    solution_cities = initial_cities
    same_solution = 0
    same_cost_diff = 0
    numberOfRepetions = 0
    
    while current_temp > 1 and same_solution < 2 and same_cost_diff < 5:
        numberOfRepetions = numberOfRepetions + 1
        altered_route = get_neighbors(solution_cities)
        # Check if neighbor is best so far
        cost_diff = get_cost(altered_route) - get_cost(solution_cities)
        # if the new solution is better, accept it
        if cost_diff > 0:
            solution_cities = altered_route
            #Setting best routes
            best_routedis = 1/get_cost(altered_route)
            best_route = altered_route
            same_solution = 0
            same_cost_diff = 0
            
        elif cost_diff == 0:
            solution_cities = altered_route
            same_solution = 0
            same_cost_diff +=1
        # if the new solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            if random.uniform(0, 1) <= math.exp(float(cost_diff) / float(current_temp)):
                solution_cities = altered_route
                same_solution = 0
                same_cost_diff = 0
            else:
                same_solution +=1
                same_cost_diff+=1
        # decrement the temperature
        current_temp = current_temp*alpha
        print(1/get_cost(solution_cities), numberOfRepetions)
    
    return (best_route, best_routedis)

def finishing_annealing(best_route):

    best_routedis = 0
    best_route = np.empty((5000, 2))

    # Start by initializing the current list with the initial list
    solution_cities = best_route
    numberOfRepetions = 0
    
    while numberOfRepetions < 1000:
        numberOfRepetions = numberOfRepetions + 1
        altered_route = get_neighbors(solution_cities)
        # Check if neighbor is best so far
        cost_diff = get_cost(altered_route) - get_cost(solution_cities)
        # if the new solution is better, accept it
        if cost_diff > 0:
            solution_cities = altered_route
            #Setting best routes
            best_routedis = 1/get_cost(altered_route)
            best_route = altered_route
            
        print(1/get_cost(solution_cities), numberOfRepetions)
    
    return (best_route, best_routedis)

def get_cost(state):
    """Calculates cost/fitness for the solution/route."""
    distance = 0
    
    for i in range(len(state)):
        from_city = state[i]
        to_city = None
        if i+1 < len(state):
            to_city = state[i+1]
        else:
            to_city = state[0]
        distance += euclidean_distance(from_city, to_city)
    fitness = 1/float(distance)
    return fitness

def euclidean_distance(pointa, pointb):
    return math.sqrt(math.pow(pointa[0] - pointb[0], 2) + math.pow(pointa[1] - pointb[1], 2))

def get_neighbors(state):
    """Returns neighbor of  your solution."""

    neighbor = copy.deepcopy(state)

    func = random.choice([1,2])  #Need to add 0 and 3 once working
    if func == 0:
        inverse(neighbor)
        
    elif func == 1:
        insert(neighbor)
        
    elif func == 2 :
        swap(neighbor)
    
    else:
        swap_routes(neighbor)
        
    return neighbor 

def inverse(state):
    "Inverses the order of cities in a route between node one and node two"
    index_j = random.choice(range(len(state)))  #Selects random index
    index_i = random.choice(range(len(state)))  #Finding new index point

    if(index_i == index_j):                     #Checks they are not the same point
        index_i = random.choice(range(len(state)))

    state[min(index_j,index_i):max(index_j,index_i)] = state[min(index_j,index_i):max(index_j,index_i)][::-1]

    return state

def insert(state):
    "Insert city at node j before node i"
    index_j = random.choice(range(len(state)))  #Selects random index
    index_i = random.choice(range(len(state)))  #Finding new index point

    if(index_i == index_j):                     #Checks they are not the same point
        index_i = random.choice(range(len(state)))
    
    del_state = np.delete(state, index_j ,0)
    state = np.insert(del_state, index_i - 1, state[index_j], 0)    #Repositioning values
    return state

def swap(state):
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