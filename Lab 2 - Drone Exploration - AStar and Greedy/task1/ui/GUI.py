import pyautogui
import time
from random import randint
from controller.Controller import Controller
from domain.Constants import *
import pygame
from pygame.locals import *


class GUI:
    def __init__(self):
        # initial coords (first we position the drone somewhere in the area
        self._initialX = randint(0, 19)
        self._initialY = randint(0, 19)
        # final coords (where the drone needs to arrive)
        self._finalX = randint(0, 19)
        self._finalY = randint(0, 19)
        self._controller = Controller(self._initialX, self._initialY)

    def start(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)

        # check if the final position is a wall
        while self._controller.get_map().surface[self._finalX][self._finalY] == 1:
            self._finalX = randint(0, 19)
            self._finalY = randint(0, 19)

        print('Start: (' + str(self._initialX) + ', ' + str(self._initialY) + ')')
        print('End: (' + str(self._finalX) + ', ' + str(self._finalY) + ')')

        # define a variable to control the main loop
        running = True

        printed_a_star = False
        printed_greedy = False
        printed_time = False

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            if not printed_a_star:
                start_a_star = time.time()
                path_a_star = self._controller.searchAStar(self._initialX, self._initialY, self._finalX, self._finalY)
                end_a_star = time.time()

            if not printed_a_star:
                print("A* path: ")
                print(path_a_star)
                printed_a_star = True

            screen.blit(self._controller.displayWithPath(self._controller.get_map().image(), path_a_star), (0, 0))

            if not printed_greedy:
                start_greedy = time.time()
                path_greedy = self._controller.searchGreedy(self._initialX, self._initialY, self._finalX, self._finalY)
                end_greedy = time.time()

            if not printed_greedy:
                print("Greedy path: ")
                print(path_greedy)
                printed_greedy = True

            screen.blit(self._controller.displayWithPath(self._controller.get_map().image(), path_greedy), (400, 0))

            if not printed_time:
                print('Execution time for A*: ' + str(end_a_star - start_a_star))
                print('\nExecution time for Greedy: ' + str(end_greedy - start_greedy))
                printed_time = True

            pygame.display.flip()

        pygame.quit()
