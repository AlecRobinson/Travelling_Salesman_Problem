'''
import turtle
import random
import math
import sys
'''
import pandas as pd  
''' # data processing, CSV file I/O (e.g. pd.read_csv)

df_cities = pd.read_csv("cities.csv",  usecols=[1,2] ,header=None, skiprows=1)
sectionOfCities = df_cities.iloc[:5000]

number_iterations = 10
number_cities = len(sectionOfCities)
tabu_length = 20
tabu_list = []
best_distance = 1000000000
distance = 0

def main():
    
    global distance

    get_arguments()

    citylocations = []

    for i in range(0,number_cities):
        #print(sectionOfCities.iat[i,0])
        citylocations.append((float(sectionOfCities.iat[i,0]), float(sectionOfCities.iat[i,1])))   

    #Setting up the turtle screen
    #screen = turtle.Screen()
    #turtle.speed(0)     #Turns animation off so turtle can go as fast as possible
    #screen.setup(width=1500,height=1000)
    #screen.title('Traveling Santa')

    #dotCities(citylocations)                #Draws out all cities
    
    # Run 50 iteration of Gradient Descent or TABU search
    for i in range(0, number_iterations):
        #citylocations = gd_iteration(citylocations)
        citylocations = tabu_iteration(citylocations)           #Running the pathfinding method
        print(distance)

    #screen.exitonclick()

def get_arguments():
    global number_cities
    global number_iterations
    global tabu_length


    print("The sys.argv list is:",sys.argv)
    # If no command line arguments supplied then
    # default and return function
    if len(sys.argv) == 1:
        print(
            f"Usage: {sys.argv[0]} <number of cities>"
            "<number of iterations> <tabu_length> <rng seed>")
        print(f"Defaulting to:\nnumber of cities={number_cities},"
              f"\nnumber of iterations={number_iterations},"
              f"\ntabu length={tabu_length}")

        return

    # If they have been supplied but cause an error
    # (are incorrect) print help and exit
    try:
        number_cities = int(sys.argv[1])
        number_iterations = int(sys.argv[2])
        tabu_length = int(sys.argv[3])
    except:
        try:
            number_cities = int(sys.argv[1])
            number_iterations = int(sys.argv[2])
            tabu_length = int(sys.argv[3])
        except:
            raise SystemExit(
                f"Usage: {sys.argv[0]} <number of cities>"
                "<number of iterations> <tabu_length> <rng seed>")


def tabu_iteration(citylocations):
    # Make sure we have write access to our
    # TABU list
    global tabu_list
    global tabu_length
    global distance

    # Create a list of candidates
    candidates = create_candidates(citylocations)

    # Get a sorted list of candidates
    # lowest (i.e. best) first
    scored_candidates = sorted(candidates, key=objective_function)

    # Check if each candidate (in order) is TABU
    # tabu check will return true if a candidate
    # is not in the list, or is in the list but
    # is allowed by aspiration criteria
    usable_candidate = None
    for scored_candidate in scored_candidates:
        if tabu_check(scored_candidate):
            usable_candidate = scored_candidate
            break

    # Draw's the current path using turtle
    distance = findDistance(usable_candidate)

    # Add current usable candidate to the tabu list
    tabu_list.append(usable_candidate)

    # While tabu list is oversize, reduce it!
    while len(tabu_list) > tabu_length:
        tabu_list.pop(0)

    # Return selected candidate
    return usable_candidate


def tabu_check(candidate):
    # Make sure we have write access to our global tabu list
    global tabu_list

    # Set our flag to true initially
    usable = True

    # Perform checks and set flag to false if needed
    for tabu_candidate in tabu_list:
        if tabu_candidate == candidate and (objective_function(tabu_list[-1]) - objective_function(tabu_candidate)) < 100:
            usable = False
            break

    # Return the flag value
    return usable


def objective_function(candidate):
    sum = 0

    for i in range(0, number_cities):
        if i == number_cities - 1:
            sum = sum + euclidean_distance(candidate[-1], candidate[0])
        else:
            sum = sum + euclidean_distance(candidate[i], candidate[i+1])

    return sum

def euclidean_distance(pointa, pointb):
    return math.sqrt(
        math.pow(pointa[0] - pointb[0], 2) + 
        math.pow(pointa[1] - pointb[1], 2))

def create_candidates(citylocations):
    candidates = []

    for i in range(0, number_cities):

        candidate = []

        if i == number_cities - 1:
            candidate.append(citylocations[-1])
            candidate.extend(citylocations[1:-1])
            candidate.append(citylocations[0])
        else:
            for j in range(0, number_cities):
                if not j == i and not j == i + 1:
                    candidate.append(citylocations[j])
                elif j == i and not i == number_cities - 1:
                    candidate.append(citylocations[i+1])
                    candidate.append(citylocations[i])

            if i == number_cities - 1:
                candidate.append(citylocations[0])

        candidates.append(candidate)

    return candidates


def drawpath(cities):
    turtle.clear()
    drawdistance(cities)
    turtle.penup()

    for city in cities:
        turtle.goto((x / 5 - 400) for x in city)        #Shrinks the vector so it can be visualised
        turtle.pendown()

    turtle.goto((x / 5 - 400) for x in cities[0])       #Shrinks the vector so it can be visualised


def dotCities(cities):
    turtle.clear()
    turtle.penup()

    for city in cities:
        print(city)
        turtle.goto(city)
        turtle.dot(5)

    turtle.goto(cities[0])


def drawdistance(cities):
    global best_distance

    turtle.penup()
    turtle.goto(0, +400)
    distance = objective_function(cities)
    turtle.write(f'Distance: {distance}', move=False,
                 align='left', font=('Arial', 8, 'normal'))
    
    turtle.penup()
    turtle.goto(-400, +400)
    if best_distance > distance:
        best_distance = distance
    turtle.write(f'Best Distance: {best_distance}', move=False,
                 align='left', font=('Arial', 8, 'normal'))

def findDistance(cities):
    distance = objective_function(cities)
    return distance

if __name__ == '__main__':
    main()
'''

import random
import math
import time
import copy
import sys

data = pd.read_csv("cities.csv")
cities = data.iloc[:5000]

best_dis = sys.maxsize
best_routefinal = []
iterations = 10

print(cities)
def main():
    global best_dis
    global best_routefinal
    global iterations
    convergence_time = []
    for i in range(0, 1):     
        i =  i + 1
        print(i)
        start = time.time()

        route, route_distance = annealing(cities)

        if(route_distance < best_dis):
            best_dis = route_distance
            best_routefinal.clear()
            best_routefinal.append(route) 

        time_elapsed = time.time() - start
        convergence_time.append(time_elapsed)
        print(convergence_time)
    print(best_dis)
    print(best_routefinal)

def annealing(initial_cities):
    """Peforms simulated annealing to find a solution"""
    best_routedis = 0
    best_route = []

    initial_temp = 5000
   
    alpha = 0.9
    
    current_temp = initial_temp

    # Start by initializing the current list with the initial list
    solution_cities = initial_cities
    same_solution = 0
    same_cost_diff = 0
    
    while same_solution < 2 and same_cost_diff < 5:
        altered_route = get_neighbors(solution_cities)
        print("Got Neighbours")
        # Check if neighbor is best so far
        cost_diff = get_cost(altered_route) - get_cost(solution_cities)
        print("Calculated Difference")
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
        print(1/get_cost(solution_cities), same_solution)
    
    return (best_route, best_routedis)

def get_cost(state):
    """Calculates cost/fitness for the solution/route."""
    distance = 0
    
    for i in range(len(state)):
        from_city = state.iloc[i]
        from_city = from_city[['X','Y']]
        #print(from_city)
        to_city = None
        if i+1 < len(state):
            to_city = state.iloc[i+1]
            to_city = to_city[['X','Y']]
        else:
            to_city = state.iloc[0]
            to_city = to_city[['X','Y']]
        distance += euclidean_distance(from_city.tolist(), to_city.tolist())
    fitness = 1/float(distance)
    return fitness

def euclidean_distance(pointa, pointb):
    #print(pointa)
    #print(pointb)

    return math.sqrt(
        math.pow(pointa[0] - pointb[0], 2) + 
        math.pow(pointa[1] - pointb[1], 2))

def get_neighbors(state):
    """Returns neighbor of  your solution."""

    neighbor = copy.deepcopy(state)

    func = random.choice([1,2])  #Need to add in 0 and 3 once working
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
   
    node_one = random.choice(state)
    print(node_one)
    new_list = list(filter(lambda city: city != node_one, state)) #route without the selected node one
    node_two = random.choice(new_list)
    state[min(node_one,node_two):max(node_one,node_two)] = state[min(node_one,node_two):max(node_one,node_two)][::-1]
    
    return state

def insert(state):
    "Insert city at node j before node i"
    index_j = random.choice(range(len(state)))  #Selects random index
    node_j = state.iloc[index_j]                #Finds the values at the index point
    state = state.drop([index_j])               #Deletes the vaules from dataframe

    
    index_i = random.choice(range(len(state)))  #Finding new index point
    if(index_i == index_j):                     #Checking new point has been found
        index_i = random.choice(range(len(state)))
    
    state = pd.concat([state.iloc[:index_i], node_j.to_frame().T, state.iloc[index_i:]]).reset_index(drop=True) #Inserts the values from delete point into the new selected point in dataframe
    return state

def swap(state):
    "Swaps two random cities with each other"
    pos_one = random.choice(range(len(state)))  #Selects random points in datafram
    pos_two = random.choice(range(len(state)))
    if(pos_two == pos_one):                     #Checks they are not the same point
        pos_two = random.choice(range(len(state)))
    
    state.iloc[pos_one], state.iloc[pos_two] =  state.iloc[pos_two].copy(), state.iloc[pos_one].copy()  #Switches the two points values
    return state

def swap_routes(state):
    "Select a subroute from a to b and insert it at another position in the route"
    subroute_a = random.choice(range(len(state)))
    subroute_b = random.choice(range(len(state)))
    if(subroute_a > subroute_b):
        startcity = subroute_b
        subroute = state[subroute_b:subroute_a]
        #state.drop([subroute_a,subroute_b])
    else:
        startcity = subroute_a
        subroute = state[subroute_a:subroute_b]
        #state.drop([subroute_b,subroute_a])

    insert_pos = random.choice(range(len(state)))
    for i in range(len(state)):
        print(i)
        if((i) == insert_pos):
            print(state.loc[insert_pos])
            state.loc[insert_pos + 1] = state.loc[insert_pos]
            state.loc[insert_pos] = subroute
            print(state.loc[insert_pos])
        if((i) > insert_pos):
            state[len(state) + i + 1] = state[len(state) + i]
    print(state)
    return state

if __name__ == '__main__':
    main()