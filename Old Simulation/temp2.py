import pygame
import math
pygame.init()

WIDTH, HEIGHT =  600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (160, 160, 160)
LIGHT_GREY = (230, 230, 230)
BLACK = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
MERCURY_COLOR = "#DCDBDB"
VENUS_COLOR = "#F5E16F"
EARTH_COLOR = "#79DDF2"
MARS_COLOR = "#DD4C22"
JUPITER_COLOR = "#F5CF7C"
SATURN_COLOR = "#ab604a"
URANUS_COLOR = "#7BBEF5"
NEPTUNE_COLOR = "#4b70dd"
PLUTO_COLOR = "#9ca6b7"

FONT = pygame.font.SysFont("comicsans", 16)
background = pygame.image.load("assets/gfx/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 210 / AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 day
	planet_scale = 900000000
	displacement_x = 0
	displacement_y = 0

	def __init__(self, name,  x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.name = name
		self.radius = radius
		self.color = color
		self.mass = mass

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

			#pygame.draw.lines(win, self.color, False, updated_points, 2)
		adjusted_radius = self.radius * self.SCALE * self.planet_scale
		self.image = pygame.image.load(f"assets/gfx/{self.name}.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (adjusted_radius * 2, adjusted_radius * 2))
		win.blit(self.image, (x - adjusted_radius + Planet.displacement_x, y - adjusted_radius + Planet.displacement_y))
		pygame.draw.circle(win, self.color, (x + Planet.displacement_x, y + Planet.displacement_y), self.radius)

		

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
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


def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet("Sun", 0 , 0, 30, YELLOW, 1.98892 * 10**30)
	sun.sun = True

	earth = Planet("Earth",-1 * Planet.AU ,0, 16, EARTH_COLOR, 5.9742 * 10**24)
	earth.y_vel = 29.783 * 1000 

	mars = Planet("Mars",-1.524 * Planet.AU,0, 12, MARS_COLOR, 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000

	mercury = Planet("Mercury",0.387 * Planet.AU, 0, 8, MERCURY_COLOR, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000

	venus = Planet("Venus",0.723 * Planet.AU,0, 14, VENUS_COLOR, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000

	planets = [sun, earth, mars, mercury, venus]

	while run:
		#WIN.blit(background, (0, 0))
		WIN.fill(BLACK)
		clock.tick(60)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					Planet.TIMESTEP *= 1.1
				if event.key == pygame.K_a:
					Planet.TIMESTEP /= 1.1
			
		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()