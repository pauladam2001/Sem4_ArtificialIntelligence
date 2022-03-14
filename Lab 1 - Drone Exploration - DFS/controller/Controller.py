import pygame
from domain.Environment import Environment
from domain.DMap import DMap
from domain.Drone import Drone
from domain.Constants import *


class Controller:
    def __init__(self, x, y):
        self._environment = Environment()
        self._dmap = DMap()
        self._drone = Drone(x, y)

    def get_environment(self):
        return self._environment

    def get_dmap(self):
        return self._dmap

    def get_drone(self):
        return self._drone

    # def move(self, detectedMap):
    #     pressed_keys = pygame.key.get_pressed()
    #     if self.x > 0:
    #         if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
    #             self.x = self.x - 1
    #     if self.x < 19:
    #         if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
    #             self.x = self.x + 1
    #
    #     if self.y > 0:
    #         if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
    #             self.y = self.y - 1
    #     if self.y < 19:
    #         if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
    #             self.y = self.y + 1

    def moveDFS(self):
        self._drone.visited.append((self._drone.get_x(), self._drone.get_y()))      # append to stack the current position

        # find the next possible move
        for direction in DIRECTIONS:    # up, right, left, down
            if 0 <= self._drone.get_x() + direction[0] <= 19 and 0 <= self._drone.get_y() + direction[1] <= 19:  # check that the drone is within the map
                if self._dmap.get_surface()[self._drone.get_x() + direction[0]][self._drone.get_y() + direction[1]] == 0 and \
                 (self._drone.get_x() + direction[0], self._drone.get_y() + direction[1]) not in self._drone.visited:    # check that we don't hit any wall and we have not visited this square before
                    self._drone.stack.append((self._drone.get_x(), self._drone.get_y()))    # add the current position to the stack
                    self._drone.stack.append((self._drone.get_x() + direction[0], self._drone.get_y() + direction[1]))  # add the next position to the stack
                    break

        if not self._drone.stack:   # if the stack is empty the execution stops and the position of the drone is set to None
            self._drone.x = None
            self._drone.y = None
        else:
            current = self._drone.stack.pop()       # otherwise get the next position (go back one position)
            self._drone.x = current[0]
            self._drone.y = current[1]

    def markDetectedWalls_controller(self):
        return self._dmap.markDetectedWalls(self._environment, self._drone.get_x(), self._drone.get_y())

    def dmap_image_controller(self):
        return self._dmap.image(self._drone.get_x(), self._drone.get_y())

    def env_image_controller(self):
        return self._environment.image()
