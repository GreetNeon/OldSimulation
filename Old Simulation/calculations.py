import math


class Planet:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.x = x
        self.y = y


def calculate_force(planet1, planet2, g_constant):
    # Calculating the force between the 2 planets
    distance, distance_x, distance_y = calculate_distance(planet1, planet2)
    force = (g_constant * planet1.mass * planet2.mass) / (distance ** 2)
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force
    return force_x, force_y, distance


def calculate_distance(planet1, planet2):
    distance_x = planet2.x - planet1.x
    distance_y = planet2.y - planet1.y
    distance = round(math.sqrt(distance_x ** 2 + distance_y ** 2), 7)
    return distance, distance_x, distance_y

if __name__ == "__main__":
    planet1 = Planet(1, 0, 0)
    planet2 = Planet(1, 1000, 1000)
    print(calculate_distance(planet1, planet2)[0])
