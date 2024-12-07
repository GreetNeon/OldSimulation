import math
import pygame
from calculations import calculate_force

# Creating a Planet class to add planets to the simulation
class Planet:
    # Settings
    Images = None
    Outlines = None
    Dark_mode = None
    # Constants
    AU = 149.6e6 * 1000
    # Original Gravity Constant
    OG = 6.67428e-11
    # Multiplier for the gravity constant, used to alter the simulation
    g_scale = 1
    G = OG
    # Mass Multiplier, used to alter the simulation
    mass_multiplier = 1
    # Scale of the simulation
    SCALE = 250 / AU  # 1AU = 100 pixels
    # How many seconds each frame represents
    TIMESTEP = 3600 * 60
    # How many updates it takes to complete a full orbit
    planets_points = {"Sun": 1000000, "Mercury": 40, "Venus": 90, "Earth": 150, "Mars": 285, "Jupiter": 1730,
                        "Saturn": 4300, "Uranus": 14000, "Neptune": 24000, "Pluto": 32000}
    # scale of the planets on the screen
    planet_scale = 900000000
    # How many pixels the screen is displaced by
    displacement_x = 0
    displacement_y = 0

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.adjusted_radius = 0
        self.color = color
        # Original mass
        self.o_mass = mass
        self.mass = mass
        self.name = name
        self.hovered = False
        self.circle = None
        self.is_asteroid = False

        self.image = None

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        width, height = win.get_size()
        width -= 500
        # Adjusting the position of the planet to the screen
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2

        if len(self.orbit) > 2:
            # Once there is 2 points calculated in the orbit, start updating the position
            updated_points = []
            # for point in self.orbit:
            #     x, y = point
            #     x = (x * self.SCALE + width / 2) + self.displacement_x
            #     y = (y * self.SCALE + height / 2) + self.displacement_y
            #     updated_points.append((x, y))
            if self.is_asteroid is False:
                if Planet.Outlines is True:
                    if len(updated_points) > 2:
                    # If visual orbits enabled, Draw the orbit
                        pygame.draw.lines(win, self.color, False, updated_points, 1)
        # adjusting the radius of the planet with the scale
        self.adjusted_radius = self.radius * self.SCALE * self.planet_scale

        self.circle = pygame.draw.circle(win, self.color, (x, y), self.adjusted_radius)

        if self.is_asteroid is False:
            if Planet.Images is True:
                # If planet images enabled, draw the image
                self.image = pygame.transform.smoothscale(
                    pygame.image.load(f"assets/gfx/{self.name}.png").convert_alpha(),
                    ((self.adjusted_radius * 2), self.adjusted_radius * 2))

                win.blit(self.image, (x - self.adjusted_radius, y - self.adjusted_radius))


    def attraction(self, other_planet):
        # Calculating the force between the planet and another planet
        force_x, force_y, distance = calculate_force(self, other_planet, self.G)
        if other_planet.sun:
            self.distance_to_sun = distance
        return force_x, force_y


    def update_position(self, planets):
        # Updating the position of the planet
        if self.is_asteroid is False:
            while len(self.orbit) > self.planets_points[self.name]:
                del (self.orbit[0])

        total_fx = total_fy = 0
        for planet in planets:
            # Calculating the force between the planet and all other planets
            if self == planet:
                # If the planet is the same as the other planet, skip it
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Calculating the new position of the planet
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        # Adding the new position to the orbit
        self.orbit.append((self.x, self.y))
        self.update_values()

    def clicked(self, point):
        # Checking if the planet is clicked
        if self.circle is not None:
            return self.circle.collidepoint(point)
        else:
            return False

    def update_values(self):
        # Updating the constants values of the simulation
        self.G = self.OG * self.g_scale
        self.mass = self.o_mass * self.mass_multiplier
        return

class Buttons:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Draw the button
    def draw(self, image, win):
        button = pygame.transform.smoothscale(pygame.image.load(image), (self.width, self.height))
        win.blit(button, (self.x, self.y))

    # Check if the mouse is hovering over the button
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(point)
    
if __name__ == "__main__":
    win = pygame.display.set_mode((500, 500))
    button = Buttons(0, 0, 100, 100, "test")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    print("clicked")
        win.fill((255, 255, 255))
        button.draw("assets/gfx/mute.png", win)
        pygame.display.update()