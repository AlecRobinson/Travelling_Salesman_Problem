import turtle
import random
import math
import sys

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

df_cities = pd.read_csv("cities.csv",  usecols=[1,2] ,header=None, skiprows=1)
sectionOfCities = df_cities.iloc[:5000]

rng_seed = None
number_iterations = 10
number_cities = len(sectionOfCities)
tabu_length = 20
tabu_list = []
best_distance = 1000000000
distance = 0

def main():
    
    global rng_seed
    global distance

    get_arguments()

    # Could add a fixed seed for debugging
    #random.seed(rng_seed)
    rng_seed = 41
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
    global rng_seed
    global tabu_length

    # If no command line arguments supplied then
    # default and return function
    if len(sys.argv) == 1:
        print(
            f"Usage: {sys.argv[0]} <number of cities>"
            "<number of iterations> <tabu_length> <rng seed>")
        print(f"Defaulting to:\nnumber of cities={number_cities},"
              f"\nnumber of iterations={number_iterations},"
              f"\ntabu length={tabu_length},"
              f"\nrng seed={rng_seed}")

        return

    # If they have been supplied but cause an error
    # (are incorrect) print help and exit
    try:
        number_cities = int(sys.argv[1])
        number_iterations = int(sys.argv[2])
        tabu_length = int(sys.argv[3])
        rng_seed = int(sys.argv[4])
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
    print(pointa, pointb)
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

'''
def dotCities(cities):
    turtle.clear()
    turtle.penup()

    for city in cities:
        print(city)
        turtle.goto(city)
        turtle.dot(5)

    turtle.goto(cities[0])
'''

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