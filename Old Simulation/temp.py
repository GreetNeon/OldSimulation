import pygame
from run_GUI import start_menu
from simulation_classes import Planet
pygame.init()
WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
MERCURY_COLOR = "#DCDBDB"
VENUS_COLOR = "#F5E16F"
EARTH_COLOR = "#79DDF2"
MARS_COLOR = "#DD4C22"
JUPITER_COLOR = "#F5CF7C"
SATURN_COLOR = "#ab604a"
URANUS_COLOR = "#7BBEF5"
NEPTUNE_COLOR = "#4b70dd"
PLUTO_COLOR = "#9ca6b7"
YELLOW = "#ffff00"

def set_planets():
    # A function to create all planet objects
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 8, EARTH_COLOR, 5.9722 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 6, MARS_COLOR, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 4, MERCURY_COLOR, 3.30 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 7, VENUS_COLOR, 4.8685 * 10 ** 24, "Venus")
    venus.y_vel = -35.02 * 1000

    planets = [sun, mercury, venus, earth, mars]
    return planets
planets = set_planets()
FPS = 60
clock = pygame.time.Clock()
def main():
    clock.tick(FPS)
    while True:
        win.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu()
        for planet in planets:
            planet.update_position(planets)
            planet.draw(win)
        pygame.display.update()
        

if __name__ == "__main__":
    main()