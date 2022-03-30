import pygame
from domain.Map import Map
from domain.Drone import Drone
from domain.Constants import *


class Controller:
    def __init__(self, x, y):
        self._map = Map()
        self._drone = Drone(x, y)

    def get_map(self):
        return self._map

    def get_drone(self):
        return self._drone

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self._drone.x > 0:
            if pressed_keys[pygame.K_UP] and self._map.surface[self._drone.x - 1][self._drone.y] == 0:
                self._drone.x = self._drone.x - 1
        if self._drone.x < 19:
            if pressed_keys[pygame.K_DOWN] and self._map.surface[self._drone.x + 1][self._drone.y] == 0:
                self._drone.x = self._drone.x + 1

        if self._drone.y > 0:
            if pressed_keys[pygame.K_LEFT] and self._map.surface[self._drone.x][self._drone.y - 1] == 0:
                self._drone.y = self._drone.y - 1
        if self._drone.y < 19:
            if pressed_keys[pygame.K_RIGHT] and self._map.surface[self._drone.x][self._drone.y + 1] == 0:
                self._drone.y = self._drone.y + 1

    # It is nothing but the sum of absolute values of differences in the goal’s x and y coordinates and the current cell’s x and y
    # coordinates respectively
    def ManhattanDistanceHeuristic(self, x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def buildPath(self, prev, finalX, finalY):
        path = [(finalX, finalY)]
        coord = prev[(finalX, finalY)]
        while coord != (None, None):
            path.append(coord)
            coord = prev[coord]
        path.reverse()
        return path

    def searchAStar(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []
        visitQueue = [(initialX, initialY)]

        prev = dict()
        prev[(initialX, initialY)] = (None, None)

        nrSteps = dict()
        nrSteps[(initialX, initialY)] = 0

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node == (finalX, finalY):
                found = True
            else:
                aux = []

                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    if -1 < newX < 20 and -1 < newY < 20 and self._map.surface[newX][newY] == 0 and (newX, newY) not in visited:
                        if (newX, newY) not in visitQueue:
                            aux.append((newX, newY))
                            prev[(newX, newY)] = node
                            nrSteps[(newX, newY)] = nrSteps[node] + 1
                        else:
                            if nrSteps[(newX, newY)] > nrSteps[node] + 1:
                                visitQueue.remove((newX, newY))
                                aux.append((newX, newY))
                                prev[(newX, newY)] = node
                                nrSteps[(newX, newY)] = nrSteps[node] + 1

                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: self.ManhattanDistanceHeuristic(coord[0], coord[1], finalX, finalY) + nrSteps[coord])

        if found:
            return self.buildPath(prev, finalX, finalY)
        else:
            return []

    def searchGreedy(self, initialX, initialY, finalX, finalY):
        found = False
        visited = []
        visitQueue = [(initialX, initialY)]

        prev = dict()
        prev[(initialX, initialY)] = (None, None)

        while visitQueue and not found:
            node = visitQueue.pop(0)
            visited.append(node)

            if node == (finalX, finalY):
                found = True
            else:
                aux = []

                for d in directions:
                    newX = node[0] + d[0]
                    newY = node[1] + d[1]

                    if -1 < newX < 20 and -1 < newY < 20 and self._map.surface[newX][newY] == 0 and (newX, newY) not in visited:
                        aux.append((newX, newY))
                        prev[(newX, newY)] = node

                visitQueue.extend(aux)
                visitQueue.sort(key=lambda coord: self.ManhattanDistanceHeuristic(coord[0], coord[1], finalX, finalY))

        if found:
            return self.buildPath(prev, finalX, finalY)
        else:
            return []

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self._drone.get_y() * 20, self._drone.get_x() * 20))

        return mapImage

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image
