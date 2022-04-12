from domain.ant import Ant, Path
from domain.map import Map
from constants import *
import numpy
import random


class Controller:
    def __init__(self, screen, map=Map()):
        self.sensors_visibility = {}
        self.ant_count = 20
        self.map = map
        self.compute_sensors()
        self.g_costs = numpy.full((map.n, map.m), numpy.inf)
        self.f_costs = numpy.full((map.n, map.m), numpy.inf)
        self.screen = screen
        self.min_dist_between_sensors = {}
        self.pheromone_level_between_sensors = {}

    # Step 2. Determine the minimum distance between each pair of sensors (using A*)
    def compute_min_dist_between_sensors(self):
        sensors = self.map.sensors
        for i in range(len(sensors) - 1):
            for j in range(i + 1, len(sensors)):  # compute the distance between the 2 sensors with A*
                path = Path(self.searchAStar(sensors[i][0], sensors[i][1], sensors[j][0], sensors[j][1]))
                self.min_dist_between_sensors[(sensors[i], sensors[j])] = path
                self.pheromone_level_between_sensors[(sensors[i], sensors[j])] = 0

        return self.min_dist_between_sensors

    # for iterations
    def run(self, rho=0.1, iterations=200):
        self.compute_min_dist_between_sensors()
        best_ant = -1
        paths = self.min_dist_between_sensors

        for k in range(iterations):
            minimum = numpy.inf
            for _ in range(self.ant_count):
                ant_path, energy_left = self.compute_one_ant()
                if k == iterations - 1:
                    res = []
                    for i in range(len(ant_path) - 1):
                        key = (ant_path[i], ant_path[i + 1])
                        if key not in paths:
                            key = (ant_path[i + 1], ant_path[i])
                            res.extend(paths[key].path[::-1])       # reverse the path
                        else:
                            res.extend(paths[key].path)

                    if minimum > len(res):
                        minimum = len(res)
                        best_one = res
                        best_ant = (ant_path, energy_left)

            for key in self.pheromone_level_between_sensors:
                self.pheromone_level_between_sensors[key] *= rho    # decrease the pheromone level by rho after each iteration (it will 'evaporate')

        self.seen_by_sensors(best_ant[0], best_ant[1])

        return best_one

    # Step 1. Determine for each sensor the number of squares that can be seen for an energy between 0 and 5
    def compute_sensors(self):
        sensors = self.map.sensors
        visibility = {}        # mapping between each sensor and the list of how much it can see

        for sensor in sensors:
            seen = [0, 0, 0, 0, 0]      # first position is 0 by default beause it can not see with energy 0
            x = sensor[0]
            y = sensor[1]

            for d in directions:
                for i in range(1, 6):
                    new_x = x + d[0] * i
                    new_y = y + d[1] * i

                    if 0 <= new_x < self.map.n and 0 <= new_y < self.map.m and self.map.surface[new_x][new_y] == 0:
                        seen[i - 1] += 1
                    else:
                        break

            visibility[sensor] = seen

        self.sensors_visibility = visibility

    @staticmethod
    def path(parents, start_node, final_node):
        current_node = parents[final_node]
        path = [final_node]

        while current_node != start_node:
            path.append(current_node)
            current_node = parents[current_node]

        path.append(start_node)
        path.reverse()

        return path

    @staticmethod
    def best_node(nodes):
        queue = list(nodes.keys())
        best_index = 0

        for i in range(len(queue)):
            if nodes[queue[i]] < nodes[queue[best_index]]:
                best_index = i

        return queue[best_index]

    @staticmethod
    def ManhattanDistanceHeuristic(x, y, finalX, finalY):
        return abs(finalX - x) + abs(finalY - y)

    # calculate the distance between 2 sensors
    def searchAStar(self, initialX, initialY, finalX, finalY):
        current_node = (initialX, initialY)
        open_nodes = {(initialX, initialY): 0}
        visited = []
        parents = {}

        while len(open_nodes) > 0:
            current_node = self.best_node(open_nodes)
            del open_nodes[current_node]
            visited.append(current_node)

            if current_node[0] == finalX and current_node[1] == finalY:
                return self.path(parents, (initialX, initialY), current_node)

            for d in directions:
                x = current_node[0] + d[0]
                y = current_node[1] + d[1]
                if (x, y) not in visited:
                    if 0 <= x < self.map.n and 0 <= y < self.map.m:
                        if self.map.surface[x][y] == 0 or self.map.surface[x][y] == 2:
                            if self.g_costs[current_node[0]][current_node[1]] + 1 < self.g_costs[x][y] or (x, y) not in open_nodes:
                                self.f_costs[x][y] = self.g_costs[current_node[0]][current_node[1]] + 1 + self.ManhattanDistanceHeuristic(x, y, finalX, finalY)
                                parents[(x, y)] = current_node
                                if (x, y) not in open_nodes:
                                    open_nodes[(x, y)] = self.f_costs[x][y]
        return []

    # iteration for an ant
    def compute_one_ant(self):
        first_sensor = random.choice(self.map.sensors)
        ant = Ant(first_sensor)
        sensors_order = [first_sensor]

        for _ in range(len(self.map.sensors) - 1):
            new_sensor = ant.choose_sensor(self.min_dist_between_sensors, self.pheromone_level_between_sensors, self.sensors_visibility)
            if new_sensor != "No more sensors":
                sensors_order.append(new_sensor)

        return sensors_order, ant.energy

    # Step 4. Determine using any method the quantity of energy that is left there
    def seen_by_sensors(self, sensors_order, energy_left):
        # print("Energy left:", energy_left)

        count = 0
        left_to_each_sensor = [0 for _ in range(len(sensors_order))]

        while energy_left:
            sensor = -1
            maximum_visibility_for_one_sensor = 0

            for i in range(len(sensors_order)):
                if left_to_each_sensor[i] < 4:
                    seen_count = self.sensors_visibility[sensors_order[i]][left_to_each_sensor[i]]

                    if seen_count > maximum_visibility_for_one_sensor:
                        maximum_visibility_for_one_sensor = seen_count
                        sensor = i

            if sensor == -1:
                break

            left_to_each_sensor[sensor] += 1
            count += maximum_visibility_for_one_sensor
            energy_left -= 1

        seen_squares = set()

        for sensor in sensors_order:
            for d in directions:
                for e in range(1, left_to_each_sensor[sensors_order.index(sensor)] + 1):
                    x = sensor[0] + d[0] * e
                    y = sensor[1] + d[1] * e
                    if 0 <= x < self.map.n and 0 <= y < self.map.m and self.map.surface[x][y] == 0:     # where the sensors can see
                        seen_squares.add((x, y))
                        self.map.surface[x][y] = 3
                    else:
                        break

        # print("Seen:", len(seen_squares))
        print("Sensors order:", sensors_order)
        # print("Left to sensors:", left_to_each_sensor)

        return count, sensors_order, left_to_each_sensor
