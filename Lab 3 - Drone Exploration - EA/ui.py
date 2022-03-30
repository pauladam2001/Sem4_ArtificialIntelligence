# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *
from time import *
import matplotlib.pyplot
from utils import *
import random

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATTENTION! the function doesn't check if the path passes trough walls


class UI:
    def __init__(self):
        self.__isRunning = True
        self.__repository = Repository()
        self.__populationSize = 80
        self.__individualSize = 15
        self.__startPos = (0, 6)
        self.__bestIndividualsNr = 40
        self.__maxIterations = 300
        self.__dummyMap = Map()
        self.__dummyMap.randomMap()
        self.__controller = Controller([self.__repository, self.__populationSize, self.__individualSize, self.__startPos, self.__bestIndividualsNr, self.__maxIterations, self.__dummyMap])
        self.__stoppingFitness = 1000
        self.__lastBest = Individual()
        self.__statistics = []

        self.__repository.cmap = self.__dummyMap

        self.__lastRunStartTime = time()
        self.__lastRunEndTime = time()

    @staticmethod
    def print_menu():
        print("1. Map options:")
        print("\ta. Create a random map;")
        print("\tb. Load a map;")
        print("\tc. Save current map;")
        print("\td. Visualize map;")
        print("\te. Set start position.")
        print()
        print("2. EA options:")
        print("\tf. Parameters setup;")
        print("\tg. Run solver;")
        print("\th. Visualize the statistics;")
        print("\ti. Visualize the average and standard deviation for 30 runs;")
        print("\tj. View last best path;")
        # print("\tj. View all best paths;")
        print("\tk. View specific best path.")
        print("0. Exit.")

    def create_random_map(self):
        self.__repository.createRandomMap()

    def load_map(self):
        fileName = input("Enter file name: ")
        self.__repository.load_map_from_file(fileName)
        self.__dummyMap = self.__repository.getMap()

    def save_map(self):
        fileName = input("Enter file name: ")
        self.__repository.save_map_to_file(fileName)

    def view_map(self):
        visualize(self.__repository.cmap, self.__startPos[0], self.__startPos[1])

    def set_start_position(self):
        print(f"Current start position is: {self.__startPos}")
        print()

        x = int(input("X: "))
        y = int(input("Y: "))
        self.__startPos = (x, y)

    def parameters_setup(self):
        print("Current parameters:{")
        print(f"Population size: {self.__populationSize}")
        print(f"Battery life: {self.__individualSize}")
        print(f"Starting position: {self.__startPos}")
        # print(f"Top individuals number: {self.__bestIndividualsNr}")
        print(f"Max iterations: {self.__maxIterations}")
        print(f"Stopping fitness: {self.__stoppingFitness}")
        print("}")
        print()

        self.__populationSize = int(input("Enter population size: "))
        self.__individualSize = int(input("Enter battery life: "))
        self.__bestIndividualsNr = int(self.__populationSize / 2)
        self.__maxIterations = float(input("Enter max iterations: "))
        self.__stoppingFitness = int(input("Enter stopping fitness: "))

    def run_solver(self):
        controllerArgs = [self.__repository, self.__populationSize, self.__individualSize, self.__startPos, self.__bestIndividualsNr, self.__maxIterations, self.__dummyMap]
        self.__controller = Controller(controllerArgs)

        solverArgs = [self.__stoppingFitness]

        (self.__lastBest, self.__statistics, self.__lastRunStartTime, self.__lastRunEndTime) = self.__controller.solver(solverArgs)

        print("Execution time: ", self.__lastRunEndTime - self.__lastRunStartTime)

    def validate(self, runs):
        fitnesses = []

        for run in range(runs):
            print("masdmnasdjigasbudbuk")
            seed = random.randint(0, 10000)
            random.seed(seed)

            solverArgs = [self.__stoppingFitness]

            (_, self.__statistics, _, _) = self.__controller.solver(solverArgs)
            fitnesses.append(np.average(self.__statistics))
            print(f'Run: {run + 1} | Seed: {seed} | Fitness: {fitnesses[-1]}')

        print(f'Average: {np.average(fitnesses)}')
        print(f'Standard deviation: {np.std(fitnesses)}')

    def view_stats(self):
        print(f"Last best path: {self.__lastBest.getPath()}")
        print(f"Fitnesses: {self.__statistics}")

        average = np.average(self.__statistics)
        deviation = np.std(self.__statistics)

        print(f"Average: {average}")
        print(f"Deviation: {deviation}")

        matplotlib.pyplot.plot(range(0, len(self.__statistics)), self.__statistics)
        matplotlib.pyplot.show()

    def view_last_best_path(self):
        print(self.__lastBest.getPath())

        movingDrone(self.__repository.getMap(), self.__controller.convertMovesToPositions(self.__lastBest.getPath()))

    def view_all_best_paths(self):
        bestIndividuals = self.__controller.getBestIndividuals()

        for i in range(len(bestIndividuals)):
            print(f"{i}: {bestIndividuals[i].getPath()}")

    def view_specific_path(self):
        index = int(input("Enter iteration number: "))
        bestIndividuals = self.__controller.getBestIndividuals()
        movingDrone(self.__repository.getMap(), self.__controller.convertMovesToPositions(bestIndividuals[index].getPath()))

    def start(self):
        while True:
            self.print_menu()
            option = input("Option: ")

            if option == "a":
                self.create_random_map()
            elif option == "b":
                self.load_map()
            elif option == "c":
                self.save_map()
            elif option == "d":
                self.view_map()
            elif option == "e":
                self.set_start_position()
            elif option == "f":
                self.parameters_setup()
            elif option == "g":
                self.run_solver()
            elif option == "h":
                self.view_stats()
            elif option == "i":
                self.validate(30)
            # elif option == "j":
            #     self.view_all_best_paths()
            elif option == "j":
                self.view_last_best_path()
            elif option == "k":
                self.view_specific_path()
            elif option == "0":
                print("See you later!")
                break
            else:
                print("Please introduce a valid option!")
                print()
