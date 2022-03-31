# -*- coding: utf-8 -*-

import pickle
from random import *
from utils import *
import numpy as np
import copy

# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation


class Gene:
    def __init__(self):
        self._gene = randint(0, 3)      # a direction


class Individual:                       # a member of the population (a possible solution)
    def __init__(self, size=0, startXPosition=0, startYPosition=0):
        self.__size = size
        # self.__chromosome = [Gene() for i in range(self.__size)]     # an individual has as many genes as the individual size
        self.__chromosome = [randint(0, 3) for i in range(self.__size)]
        self.__fitness = 0
        self.__x = startXPosition
        self.__y = startYPosition

    def __lt__(self, other):
        return self.__fitness < other.__fitness
        
    def fitness(self, map):  # the capacity of a genotype to be propagated into future generations, reflects the adaptation to environment
        # compute the fitness for the individual
        # and save it in self.__f

        # if we hit a wall we decrease a fitness by 20, if we go out of bouns we deacrease it by 10, we increase it by one whit every position that
        # we can visit, and we increase it by 900 when i > size/2 and we have been only in one direction without hitting a wall

        self.__fitness = 0

        moves = self.__chromosome

        x = self.__x
        y = self.__y

        surface = map.getSurface()

        enteredWall = False

        for i in range(self.__size):
            if surface[x][y] == 1:
                self.__fitness -= 20
                enteredWall = True
            elif x < 0 or x > mapLength - 1 or y < 0 or y > mapLength - 1:
                enteredWall = True
                self.__fitness -= 10
            # elif i > self.__size / 2 and (not enteredWall) and x == self.__x and y == self.__y:
            #     self.__fitness += 900
            else:
                positiveGain = self.checkArea(surface, x, y)
                self.__fitness += positiveGain

            # if moves[i] == UP and surface[x - 1][y] != 1:
            #     x -= 1
            # elif moves[i] == LEFT and surface[x][y - 1] != 1:
            #     y -= 1
            # elif moves[i] == DOWN and surface[x + 1][y] != 1:
            #     x += 1
            # elif moves[i] == RIGHT and surface[x][y + 1] != 1:
            #     y += 1
            if moves[i] == UP:
                x -= 1
            elif moves[i] == LEFT:
                y -= 1
            elif moves[i] == DOWN:
                x += 1
            elif moves[i] == RIGHT:
                y += 1

    def checkArea(self, surface, x, y):     # get the number of positions that are not walls and we can visit
        yf = 0
        xf = 0

        seenArea = 0

        # UP
        xf = x - 1
        while ((xf >= 0 and y < mapLength - 1 and y >= 0) and (surface[xf][y] != 1)):
            if (surface[xf][y] == 0):
                # print("pass up")
                seenArea += 1
            surface[xf][y] = 2
            xf = xf - 1

        # DOWN
        xf = x + 1
        while ((xf < mapLength - 1 and y < mapLength - 1 and y >= 0) and (surface[xf][y] != 1)):
            if (surface[xf][y] == 0):
                # print("pass down")
                seenArea += 1
            surface[xf][y] = 2
            xf = xf + 1
        # LEFT
        yf = y + 1
        while ((yf < mapLength - 1 and x < mapLength - 1 and x >= 0) and (surface[x][yf] != 1)):
            if (surface[x][yf] == 0):
                # print("pass left")
                seenArea += 1
            surface[x][yf] = 2
            yf = yf + 1

        # RIGHT
        yf = y - 1
        while ((yf >= 0 and x < mapLength - 1 and x >= 0) and (surface[x][yf] != 1)):
            if (surface[x][yf] == 0):
                # print("pass right")
                seenArea += 1
            surface[x][yf] = 2
            yf = yf - 1

        # print(f"Seen area: {seenArea}")
        return seenArea

    def getFitness(self):
        return self.__fitness

    def mutate(self, mutateProbability=0.04):       # reintroduces in population the lost genetic material
        if random() < mutateProbability:
            # perform a mutation with respect to the representation
            index = randint(0, self.__size - 1)
            self.__chromosome[index] = randint(0, 3)        # change the direction of a random gene
            # self.__chromosome[index] = Gene()
    
    def crossover(self, otherParent, crossoverProbability=0.8):                         # mix the parents' information
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)

        for i in range(self.__size):
            if random() < crossoverProbability:
                # perform the crossover between the self and the otherParent
                offspring1.__chromosome[i] = self.__chromosome[i]                   # one gene from a parent, one from the other one
                offspring2.__chromosome[i] = otherParent.__chromosome[i]
            else:
                offspring1.__chromosome[i] = otherParent.__chromosome[i]
                offspring2.__chromosome[i] = self.__chromosome[i]

        return offspring1, offspring2

    def getPath(self):
        return self.__chromosome


class Population:                                                 # a number of individuals (set of possible solutions)
    def __init__(self, currentMap, populationSize=0, individualSize=0, startXPosition=0, startYPosition=0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize, startXPosition, startYPosition) for x in range(populationSize)]      # a population has populationsSize individuals
        self.__individualSize = individualSize
        self.__map = currentMap

    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness(self.__map)

    def selection(self, k=0):       # for recombination, gives more reproduction/survival chances to better individuals, based on fitness only
        # perform a selection of k individuals from the population
        # and returns that selection
        self.evaluate()

        # self.__v.sort(reverse=True)
        self.__v.sort(key=lambda v: v.getFitness(), reverse=True)

        topIndividuals = self.__v[:k]

        return topIndividuals

    def getBest(self):
        # self.__v.sort(reverse=True)
        self.__v.sort(key=lambda v: v.getFitness(), reverse=True)
        return self.__v[0]

    def average_fitness(self):
        # return np.average([x.getFitness() for x in self.__v])
        avgFitness = 0
        for elem in self.__v:
            avgFitness += elem.getFitness()

        avgFitness = avgFitness / self.__populationSize

        return avgFitness

    def setIndividualsPool(self, pool):
        self.__v = pool

    def __repr__(self):
        return "Population {" + str(self.__v) + "}"


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def load_map(self, fileName):               # loads the map from the file
        with open(fileName, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def save_map(self, fileName="test.map"):     # saves the current map in the file
        with open(fileName, "wb") as f:
            pickle.dump(self, f)
            f.close()

    def getSurface(self):
        return copy.copy(self.surface)

    def setSurface(self, newSurface):
        self.surface = newSurface

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
