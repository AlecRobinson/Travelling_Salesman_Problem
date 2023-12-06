import random
import math
import time
import copy
import sys
import pandas as pd 
import numpy as np

#Read Data From CSV File
data = pd.read_csv("cities.csv", usecols=[1,2] ,header=None, skiprows=1)

#Create Global Variables
best_route = data.iloc[:5000].to_numpy()
best_dis = sys.maxsize
iterations = 5

'Main Function'
def main():
    global best_dis
    global best_route
    global iterations
    convergence_time = 0

    #Looping for number of iterations
    for i in range(0, iterations):     
        i =  i + 1
        print("Iteration Number: " + str(i))
        start = time.time()

        #Performing simulated annealing on the current best route
        route, route_distance = annealing(best_route)

        #Checking if what was found is better than what we currently have
        if(route_distance < best_dis):
            best_dis = route_distance
            best_route = route 

        #Finding time taken to perform iteration and adding it to overall time taken
        time_elapsed = time.time() - start
        convergence_time = convergence_time + time_elapsed
        print(time_elapsed)

    #Prining out best answer, route and time elapsed
    print(best_dis)
    print(best_route)
    print(convergence_time)
'Simulated annealing function'
def annealing(initial_cities):
    ann_best_routedis = best_dis
    ann_best_route = initial_cities
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
            if(1/get_cost(altered_route) < ann_best_routedis):
                ann_best_routedis = 1/get_cost(altered_route)
                ann_best_route = altered_route
            
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
    
    return (ann_best_route, ann_best_routedis)
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

    altered_state = swap_routes(neighbor)
        
    return altered_state 



def swap_routes(state):
    "Select a subroute from a to b and insert it at another position in the route"
    subroute_a = random.choice(range(len(state)))
    subroute_b = random.choice(range(len(state)))
    subroute = state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]

    print(state)

    if(subroute_a > subroute_b):
        del_state = np.delete(state, slice(subroute_b,subroute_a),0)
    else:
        del_state = np.delete(state, slice(subroute_a,subroute_b),0)
    
    print(del_state)

    insert_pos = random.choice(range(len(state)))
    while(insert_pos + len(subroute) > len(state)):
        insert_pos = random.choice(range(len(state)))

    state = np.insert(del_state, insert_pos, subroute,0)
    print(state)

    return state

if __name__ == '__main__':
    main()