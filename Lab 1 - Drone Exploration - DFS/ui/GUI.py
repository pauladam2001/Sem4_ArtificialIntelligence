import pygame
from controller.Controller import Controller
from domain.Constants import *
import time
from random import randint
import pyautogui


class GUI:
    def __init__(self):
        x = randint(0, 19)
        y = randint(0, 19)
        self._controller = Controller(x, y)

    def start(self):
        # initialize the pygame module
        pygame.init()

        # pyautogui.alert(text='Start scanning the map!', title='Hello', button='OK')

        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(self._controller.env_image_controller(), (0, 0))

        # define a variable to control the main loop
        running = True

        pyautogui.alert(text='Start scanning the map!', title='Hello', button='OK')

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            self._controller.moveDFS()
            time.sleep(SLEEP)

            if self._controller.get_drone().get_x() is None:    # if the stack is empty we stop
                running = False
                pyautogui.alert(text="Map scanned!", title="Done", button='OK')
            else:
                self._controller.markDetectedWalls_controller()
                screen.blit(self._controller.dmap_image_controller(), (400, 0))
                pygame.display.flip()

        pygame.quit()
