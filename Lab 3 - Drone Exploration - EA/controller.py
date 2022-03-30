from repository import *
from utils import *
import time


class Controller:
    def __init__(self, args):
        # args - list of parameters needed in order to create the controller
        self.__currentIteration = 0
        self.__repository = args[0]
        self.__populationSize = args[1]
        self.__individualSize = args[2]
        self.__startPos = args[3]
        self.__bestIndividualsNr = args[4]
        self.__maxIterations = args[5]
        self.__map = args[6]

    def iteration(self, args=None):
        # args - list of parameters needed in order to run the solver
        # an iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        population = args[0]
        self.__repository.cmap = self.__map

        self.__currentIteration += 1

        if self.__bestIndividualsNr % 2 != 0:
            self.__bestIndividualsNr -= 1

        bestIndividuals = self.__repository.getLastPopulation().selection(self.__bestIndividualsNr)

        offsprings = []

        for i in range(int(self.__bestIndividualsNr / 2)):
            newOffSprings = bestIndividuals[i].crossover(bestIndividuals[i + 1])
            newOffSprings[0].mutate()
            newOffSprings[1].mutate()
            offsprings.append(newOffSprings[0])
            offsprings.append(newOffSprings[1])

        offsprings.sort()       # it works because we have __lt__ overloaded in Individual

        resultIndividuals = []

        for i in range(self.__populationSize - 1):
            if i < self.__populationSize / 2:
                resultIndividuals.append(bestIndividuals[i])
            else:
                resultIndividuals.append(offsprings[i - int(self.__bestIndividualsNr)])

        newPopulation = Population(copy.copy(self.__map), self.__populationSize, self.__individualSize, self.__startPos[0], self.__startPos[1])        # TODO copy?
        newPopulation.setIndividualsPool(resultIndividuals)

        self.__repository.addPopulation(newPopulation)

        return newPopulation
        
    def run(self, args=None):
        # args - list of parameters needed in order to run the solver
        # until stop condition
        #    perform an iteration
        #    save the information need it for the statistics
        
        # return the results and the info for statistics
        if args is None:
            args = []

        stoppingFitness = args[0]

        lastPopulation = self.__repository.getLastPopulation()

        bestIndividual = Individual()

        startTime = time.time()

        while self.__currentIteration < self.__maxIterations:
            print(f"Current iteration: {self.__currentIteration}")
            args[0] = lastPopulation

            lastPopulation = self.iteration(args)

            bestIndividual = lastPopulation.getBest()

            if bestIndividual.getFitness() >= stoppingFitness:
                endTime = time.time()
                return [bestIndividual, self.__repository.getFitnessTendency(), startTime, endTime]

        endTime = time.time()
        return [bestIndividual, self.__repository.getFitnessTendency(), startTime, endTime]

    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        # create the population,
        # run the algorithm
        # return the results and the statistics
        if self.__repository.getPopulationsLength() == 0:
            self.__repository.createPopulation([self.__populationSize, self.__individualSize])

        self.__currentIteration = 0

        return self.run(args)

    def getBestIndividuals(self):
        return self.__repository.getAllBest()

    def convertMovesToPositions(self, movesPath):
        x = self.__startPos[0]
        y = self.__startPos[1]

        path = []
        path.append((x, y))
        for move in movesPath:
            if move == UP:
                x -= 1
            elif move == LEFT:
                y -= 1
            elif move == DOWN:
                x += 1
            elif move == RIGHT:
                y += 1

            path.append((x, y))

        return path
