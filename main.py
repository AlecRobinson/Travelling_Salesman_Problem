import turtle
import random
import math

#

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import os

df_cities = pd.read_csv("C:/Users/Alec/Desktop/Uni Work/CT5102-Python-Optimisation/cities.csv")
df_cities.head()

citys_no_header = pd.read_csv("C:/Users/Alec/Desktop/Uni Work/CT5102-Python-Optimisation/cities.csv",  usecols=[1,2] ,header=None, skiprows=1)

#fig = plt.figure(figsize=(20,20))
#cmap, norm = from_levels_and_colors([0.0, 0.5, 1.5], ['red', 'black'])
#plt.scatter(df_cities['X'],df_cities['Y'],marker = '.',c=(df_cities.CityId != 0).astype(int), cmap='Set1', alpha = 0.6, s = 500*(df_cities.CityId == 0).astype(int)+1)
#plt.show()

#


number_cities = len(df_cities)
print(number_cities)
tabu_list = [100]

def main():
    turtle.speed(0) #Turns animation off so turtle can go as fast as possible
    random.seed(42)
    citylocations = []
    #print(citys_no_header)

    for i in range(0,number_cities):
        citylocations.append((float(citys_no_header.iat[i,0]) / 5.0 - 450, float(citys_no_header.iat[i,1]) / 5.0 - 350))
        
    screen = turtle.Screen()
    screen.setup(width=1000,height=1000)
    screen.title('Traveling Santa')
    dotCities(citylocations)                #Draws out all cities

    tabu_iteration(citylocations)

    screen.exitonclick()

def tabu_iteration(citylocations):
    candidates = create_candidates(citylocations)
    best_score = 100000000
    best_candidate = number_cities + 1

    scored_candidates = []

    scored_candidates = sorted(candidates, key=objective_function)

    for scored_candidate in scored_candidates:
        if not tabu_check(scored_candidate):
            usable_candidate = scored_candidate
            print(usable_candidate)
            break
        
    drawpath(usable_candidate)
    for i in range(0, number_cities):
        scored_candidates.append((objective_function(candidates[i]), candidates[i]))
        score = objective_function(candidates[i])
        if score < best_score:
            best_score = score
            best_candidate = i
    print(best_candidate)

    if best_candidate != candidates[0]:
        scored_candidates = sorted(candidates[best_candidate], key=objective_function)

        for scored_candidate in scored_candidates:
            if not tabu_check(scored_candidate):
                usable_candidate = scored_candidate
                print(usable_candidate)
                break
        
        drawpath(usable_candidate)
        for i in range(0, number_cities):
            scored_candidates.append((objective_function(candidates[i]), candidates[i]))
            score = objective_function(candidates[i])
            if score < best_score:
                best_score = score
                best_candidate = i
        print(best_candidate)

    drawpath(citylocations)

def tabu_check(candidate):
    global tabu_list

    match = False

    for tabu_candidate in tabu_list:
        if tabu_candidate == candidate:
           match = True 
           break

    return match


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
    turtle.penup()

    for city in cities:
        turtle.goto(city)
        turtle.pendown()

    turtle.goto(cities[0])

def dotCities(cities):
    turtle.clear()
    turtle.penup()

    for city in cities:
        print(city)
        turtle.goto(city)
        turtle.dot(5)

    turtle.goto(cities[0])

if __name__ == '__main__':
    main()