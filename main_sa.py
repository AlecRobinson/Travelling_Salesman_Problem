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
iterations = 10000


"""Main Function"""
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

    #Once all iteration are done. We perform another final annealing without a fitness to bottom out the data and find best possible route
    route, route_distance = finishing_annealing(best_route)
    if(route_distance < best_dis):
         best_dis = route_distance
         best_route = route 

    #Prining out best answer, route and time elapsed
    print(best_dis)
    print(best_route)
    print(convergence_time)


"""Simulated annealing function"""
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
    
    #Looping the alterations until 3 factors have occured
    while current_temp > 1 and same_solution < 2 and same_cost_diff < 5:
        numberOfRepetions = numberOfRepetions + 1
        altered_route = get_neighbors(solution_cities)
        
        #Check if neighbor is best so far
        cost_diff = get_cost(altered_route) - get_cost(solution_cities)
        
        #If the new solution is better accept it
        if cost_diff > 0:
            solution_cities = altered_route
            
            #Setting best routes
            if(1/get_cost(altered_route) < ann_best_routedis):
                ann_best_routedis = 1/get_cost(altered_route)
                ann_best_route = altered_route
            same_solution = 0
            same_cost_diff = 0
        
        #If the new solution is the same accept it and increment variable
        elif cost_diff == 0:
            solution_cities = altered_route
            same_solution = 0
            same_cost_diff +=1

        #If the new solution is not better accept it with a probability of e^(-cost/temp)
        else:
            if random.uniform(0, 1) <= math.exp(float(cost_diff) / float(current_temp)):
                solution_cities = altered_route
                same_solution = 0
                same_cost_diff = 0
            else:
                same_solution +=1
                same_cost_diff+=1
        
        #Decrement the temperature
        current_temp = current_temp*alpha
        print(1/get_cost(solution_cities), numberOfRepetions)
    return (ann_best_route, ann_best_routedis)


"""Simulated annealing function without temperature"""
def finishing_annealing(best_route):
    ann_best_routedis = best_dis
    ann_best_route = best_route

    #Start by initializing the current list with the initial list
    solution_cities = best_route
    numberOfRepetions = 0
    
    #Loop 100 times to bottom out the route
    while numberOfRepetions < 100:
        numberOfRepetions = numberOfRepetions + 1
        altered_route = get_neighbors(solution_cities)
        
        #Check if neighbor is best so far
        cost_diff = get_cost(altered_route) - get_cost(solution_cities)
        
        #If the new solution is better accept it
        if cost_diff > 0:
            solution_cities = altered_route
            
            #Setting best routes
            if(1/get_cost(altered_route) < ann_best_routedis):
                ann_best_routedis = 1/get_cost(altered_route)
                ann_best_route = altered_route 
        print(1/get_cost(solution_cities), numberOfRepetions)
    return (ann_best_route, ann_best_routedis)

"""Calculates cost/fitness for the solution/route."""
def get_cost(state):
    distance = 0
    
    #Loops for the length of the route
    for i in range(len(state)):
        from_city = state[i]
        to_city = None

        #Finding next city
        if i+1 < len(state):
            to_city = state[i+1]
        else:
            to_city = state[0]

        #Calculate the euclidean distance from the selected city to the next city
        distance += euclidean_distance(from_city, to_city)
    
    #Setting fitness as the reciprocal of distance
    fitness = 1/float(distance)
    return fitness

"""Calculates the euclidean distance between two coordinates"""
def euclidean_distance(pointa, pointb):
    return math.sqrt(math.pow(pointa[0] - pointb[0], 2) + math.pow(pointa[1] - pointb[1], 2))

"""Returns neighbor of  your solution."""
def get_neighbors(state):
    neighbor = copy.deepcopy(state)

    #Randomly chooses one of the 4 alterations to apply to the route
    func = random.choice([0,1,2,3])
    if func == 0:
        altered_state = inverse(neighbor)
    elif func == 1:
        altered_state = insert(neighbor)
    elif func == 2 :
        altered_state = swap(neighbor)
    else:
        altered_state = swap_routes(neighbor)
    return altered_state 

"Inverses the order of cities in a route between node one and node two"
def inverse(state):
    #Selects two random indexs
    index_j = random.choice(range(len(state)))  
    index_i = random.choice(range(len(state)))  

    #Error check they are not the same point
    while(index_i == index_j):                     
        index_i = random.choice(range(len(state)))

    #Inversing the route between node one and two
    state[min(index_j,index_i):max(index_j,index_i)] = state[min(index_j,index_i):max(index_j,index_i)][::-1]
    return state

"Insert city at node j before node i"
def insert(state):
    #Selects two random indexs
    index_j = random.choice(range(len(state))) 
    index_i = random.choice(range(len(state)))  

    #Error check they are not the same point
    while(index_i == index_j):                     
        index_i = random.choice(range(len(state)))
    
    #Deleting and repositioning the cities
    del_state = np.delete(state, index_j ,0)
    state = np.insert(del_state, index_i - 1, state[index_j], 0)
    return state

"Swaps two random cities with each other"
def swap(state):
    #Selects two random indexs
    pos_one = random.choice(range(len(state)))  
    pos_two = random.choice(range(len(state)))  
    
    #Error check they are not the same point
    while(pos_two == pos_one):                     
        pos_two = random.choice(range(len(state)))
    
    #Switching values
    state[[pos_one, pos_two]] = state[[pos_two, pos_one]] 
    return state

"Select a subroute from a to b and insert it at another position in the route"
def swap_routes(state):
    #Selects two random indexs and finding subroute
    subroute_a = random.choice(range(len(state)))
    subroute_b = random.choice(range(len(state)))
    subroute = state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]

    #Finding smaller value and deleting accourding route
    if(subroute_a > subroute_b):
        del_state = np.delete(state, slice(subroute_b,subroute_a),0)
    else:
        del_state = np.delete(state, slice(subroute_a,subroute_b),0)
    
    #Selects random index
    insert_pos = random.choice(range(len(state)))
    
    #Error check they are not the same point
    while(insert_pos + len(subroute) > len(state)):
        insert_pos = random.choice(range(len(state)))
    
    #Inserts route in position
    state = np.insert(del_state, insert_pos, subroute,0)
    return state


if __name__ == '__main__':
    main()