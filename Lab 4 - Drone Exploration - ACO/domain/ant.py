import random


class Ant:
    def __init__(self, starting_sensor, energy=150):
        self.path = []
        self.energy_given = []      # how much energy for each sensor
        self.visited_sensors = [starting_sensor]    # list of visited sensors
        self.energy = energy    # energy level

    # Step 3. Determine using ACO the shortest path between sensors
    def choose_sensor(self, distances_between_sensors, pheromone_level, sensors_visibility, alpha=0.8, beta=1.5):
        last_sensor = self.visited_sensors[-1]

        possible_sensors = []    # list of sensors that can be visited

        for sensors in distances_between_sensors:   # (sensor0, sensor1) -> Path
            if sensors[0] == last_sensor and sensors[1] not in self.visited_sensors:      # append whichever sensor has not been visited
                possible_sensors.append([sensors[1], distances_between_sensors[sensors]])
            if sensors[1] == last_sensor and sensors[0] not in self.visited_sensors:
                possible_sensors.append([sensors[0], distances_between_sensors[sensors]])

        probabilites = []

        for sensors in possible_sensors:
            key = (sensors[0], last_sensor)
            if key not in pheromone_level.keys():
                key = (last_sensor, sensors[0])

            distance = sensors[1].Length
            if distance <= self.energy:         # computes how prone the ant is to go at a specific sensor based on distance and pheromone level
                if pheromone_level[key] != 0:   # if the pheromones were placed
                    probabilites.append((1 / distance ** beta) * (pheromone_level[key] ** alpha))
                else:       # if it is first iteration and there are no pheromones
                    probabilites.append((1 / distance ** beta))

        # create the list with probabilities
        s = sum(probabilites)
        if s == 0:
            return "No more sensors"

        p = [probabilites[i] / s for i in range(len(probabilites))]
        p = [sum(p[0: i + 1]) for i in range(len(p))]

        r = random.random()
        i = 0

        while r > p[i]:
            i = i + 1           # we choose the one with good probability from roulette

        chosen_one = possible_sensors[i][0]
        self.visited_sensors.append(chosen_one)

        key = (chosen_one, last_sensor)
        if key not in pheromone_level:
            key = (last_sensor, chosen_one)

        pheromone_level[key] += 1       # update the pheromone level
        self.energy -= distances_between_sensors[key].Length    # decrease the energy by the length of the path

        return chosen_one


# class for retaining a path and the pheromone level
class Path:
    def __init__(self, path):
        self.path = path
        self.length = len(path)
        self.pheromone_level = []

    @property
    def Length(self):
        return self.length
