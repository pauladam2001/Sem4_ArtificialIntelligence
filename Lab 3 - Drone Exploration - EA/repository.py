# -*- coding: utf-8 -*-

import pickle
from domain import *
import copy


class Repository:
    def __init__(self):
        self.__populations = []
        self.__startXPosition = 0
        self.__startYPosition = 0
        self.cmap = Map()
        self.__lastPopulation = Population(self.cmap)
        
    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args
        population = Population(self.cmap, args[0], args[1], self.__startXPosition, self.__startYPosition)
        self.__populations.append(population)
        self.__lastPopulation = self.__populations[0]

        return self.__populations[0]

    def createRandomMap(self):
        self.cmap.randomMap()

    def setStartPosition(self, position):
        (self.__startXPosition, self.__startYPosition) = position

    def addPopulation(self, population):
        self.__populations.append(population)
        self.__lastPopulation = population

    def getMap(self):
        return self.cmap

    def getLastPopulation(self):
        return copy.copy(self.__lastPopulation)

    def init_random_map(self):
        self.cmap.randomMap()

    def save_map_to_file(self, fileName="try.map"):
        self.cmap.save_map(fileName)

    def load_map_from_file(self, fileName="try.map"):
        self.cmap.load_map(fileName)

    def getPopulation(self):
        return self.__populations

    def getPopulationsLength(self):
        return len(self.__populations)

    def getFitnessTendency(self):       # get populations based on average fitness
        fitnessPopulations = []

        for i in range(len(self.__populations)):
            population = self.__populations[i]
            fitnessPopulations.append(population.average_fitness())

        return fitnessPopulations

    def getAllBest(self):           # get the best individuals from all populations
        bestIndividuals = []

        for elem in self.__populations:
            bestIndividuals.append(elem.getBest())

        return bestIndividuals
