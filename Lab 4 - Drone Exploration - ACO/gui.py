from controller import Controller
from constants import *
from domain.map import Map
import random
import pygame
import time


class GUI:
    def __init__(self):
        self.n = 20
        self.m = 20
        self.map = Map(self.n, self.m)

    def start(self):
        pygame.init()

        screen = pygame.display.set_mode((20 * self.n, 20 * self.m))
        screen.fill(WHITE)
        pygame.display.flip()

        self.map.randomMap()            # random map

        sensors = []
        for i in range(5):                          # choose the sensors randomly
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.m - 1)
            sensors.append((x, y))

        self.map.Sensors = sensors

        controller = Controller(screen, self.map)

        best_path = controller.run()

        screen.blit(self.map.image_path([]), (0, 0))
        pygame.display.flip()

        time.sleep(3)

        for i in range(len(best_path)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.time.delay(100)
            solution = best_path[:i]
            screen.blit(self.map.image_path(solution), (0, 0))
            pygame.display.flip()
            pygame.display.update()

        time.sleep(10)
