import pygame
import numpy as np


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # stack and visited are used for moveDFS
        self.stack = [(self.x, self.y)]
        self.visited = []

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_stack(self):
        return self.stack

    def get_visited(self):
        return self.visited
