import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
TEXT_COLOR = (0, 0, 0)
JUPITER_COLOR = "#bcafb2"
SATURN_COLOR = "#ab604a"
URANUS_COLOR = "#e1eeee"
NEPTUNE_COLOR = "#4b70dd"
PLUTO_COLOR = "#9ca6b7"

FONT = pygame.font.SysFont("comicsans", 12)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 60
    planets_points = {"Sun": 10, "Mercury": 40, "Venus": 90, "Earth": 150, "Mars": 285, "Jupiter": 1730,
                      "Saturn": 4300, "Uranus": 14000, "Neptune": 24000, "Pluto": 32000}

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius * self.SCALE * 900000000)

        #if not self.sun:
            #distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 5)}km", 1, WHITE)
            #win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))
        name_text = FONT.render(self.name, True, TEXT_COLOR)
        win.blit(name_text, (x - name_text.get_width() / 2, y - name_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        if len(self.orbit) > (self.planets_points[self.name]):
            del (self.orbit[0])

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def clicked(self, point):
        return pygame.Rect((self.x * self.SCALE + WIDTH / 2) - self.radius, (self.y * self.SCALE + HEIGHT / 2) - self.radius , self.radius * self.SCALE * 900000000 * 2,
                           self.radius * self.SCALE * 900000000 * 2).collidepoint(point)



def main():
    base = 0
    run = True
    clock = pygame.time.Clock()
    # 30
    sun = Planet(base, base, 30, YELLOW, 1.98892 * 10 ** 30, "Sun")
    sun.sun = True
    # 16
    earth = Planet(-1 * Planet.AU, 0, 8, BLUE, 5.9722 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000
    # 12
    mars = Planet(-1.524 * Planet.AU, 0, 6, RED, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000
    # 8
    mercury = Planet(0.387 * Planet.AU, 0, 4, DARK_GREY, 3.30 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    # 28
    venus = Planet(0.723 * Planet.AU, 0, 7, WHITE, 4.8685 * 10 ** 24, "Venus")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 20, JUPITER_COLOR, 1.898 * 10 ** 27, "Jupiter")
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 16, SATURN_COLOR, 5.683 * 10 ** 26, "Saturn")
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(-19.8 * Planet.AU, 0, 12, URANUS_COLOR, 8.681 * 10 ** 25, "Uranus")
    uranus.y_vel = 6.80 * 1000

    neptune = Planet(30 * Planet.AU, 0, 12, NEPTUNE_COLOR, 102.409 * 10 ** 24, "Neptune")
    neptune.y_vel = -5.43 * 1000

    pluto = Planet(-39 * Planet.AU, 0, 2, PLUTO_COLOR, 0.01303 * 10 ** 24, "Pluto")
    pluto.y_vel = 4.67 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

    background = pygame.image.load("back.jpg")

    pygame.key.set_repeat(1)
    background_w = 3000
    background_h = 3000
    time_passed = 0

    while run:
        clock.tick(120)

        time_passed += Planet.TIMESTEP
        time_passed_text = FONT.render(f"Time Passed: {round((time_passed / 86400) / 365, 1)} Years Or {int(round((time_passed /86400), 0))} Days",
                                       True, WHITE)
        timescale_display = FONT.render(f"Timescale: {round(Planet.TIMESTEP / 86400, 2)} Days Per Frame", True, WHITE)
        frame_display = FONT.render(f"FPS: {round(clock.get_fps(), 2)}", True, WHITE)
        backgroundimg = pygame.transform.scale(background, (background_w, background_h))
        WIN.blit(backgroundimg, (0, 0))
        WIN.blit(timescale_display, (0, 0))
        WIN.blit(frame_display, (0, 15))
        WIN.blit(time_passed_text, (0, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if Planet.SCALE < 2.5e-8:
                        Planet.SCALE *= 1.0005
                        background_w += 0.3
                        background_h += 0.3
                elif event.key == pygame.K_s:
                    if Planet.SCALE > 6e-11:
                        Planet.SCALE /= 1.0005
                        background_w -= 0.3
                        background_h -= 0.3

                elif event.key == pygame.K_a:
                    Planet.TIMESTEP /= 1.0005
                    for point in Planet.planets_points.values():
                        point *= 1.0005

                elif event.key == pygame.K_d:
                    Planet.TIMESTEP *= 1.0005
                    for point in Planet.planets_points.values():
                        point /= 1.0005
                        print(f"point {point}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                print(mouse_pos)
                for planet in planets:
                    print(planet.clicked(mouse_pos))
                        #print(planet.name)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()

# To add
# Faster = fewer points
# Settings
# Pause
# Music
# Other systems
# Make your own system
