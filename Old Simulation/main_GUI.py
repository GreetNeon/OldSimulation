import pygame

import sys
import random
from pickle_editor import load
from run_GUI import start_menu
import pygame_widgets as pw
from pygame_widgets import slider as sl
from pygame_widgets import textbox as tb
from simulation_classes import Planet, Buttons


# Pygame Init
pygame.init()
pygame.display.init()

# Window Setup
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH + 500, HEIGHT))

# Window Title
pygame.display.set_caption("Planet Simulation")

# All Colours Needed
WHITE = (255, 255, 255)
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

start_year = 2000

SIDE_WINDOW = pygame.Rect(1000, 0, 500, 1000)

# Creating a font dictionary
FONT_12 = pygame.font.SysFont("comicsans", 12)
fonts = {12: FONT_12}


# Creating a button class




def display_text(text, x, y, size, colour):
    # Displaying text on the screen
    try:
        font = fonts[size]
    except KeyError:
        # If a font with the same size is not in the dictionary, add it
        fonts[size] = pygame.font.Font('assets/font/impact.ttf', size)
        font = fonts[size]
    message = font.render(text, True, colour)
    WIN.blit(message, (x, y))


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

    # Adding all the planets to a list
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]
    return planets


def main():
    global planet_clicked, temp

    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
    # Loading the settings
    settings_file = "data/settings.pickle"
    user_settings = load(settings_file)
    Planet.Images, Planet.Outlines, background_use = (True, True, True)

    # Setting important variables
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    start_sim = True
    planets = []
    music = 0
    planet_info = 0
    pause = 0
    settings = True
    background_w = 1500
    background_h = 1500
    time_passed = 0

    # Loading the background image
    background = pygame.image.load("temp.jpg").convert()

    # Allows controls to be held down
    pygame.key.set_repeat(1)

    # Loading the  background music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sfx/space.mp3")

    # Creating all the button objects
    pause_button = Buttons(1.23 * WIDTH, 0.005 * HEIGHT, 0.04 * WIDTH, int(0.040 * HEIGHT), "Pause")
    mute_button = Buttons(1.45 * WIDTH, 0.003 * HEIGHT, 0.04 * WIDTH, int(0.040 * HEIGHT), "Mute")
    settings_button = Buttons(1.01 * WIDTH, 0.005 * HEIGHT, 0.04 * WIDTH, int(0.040 * HEIGHT), "Settings")
    restart_button = Buttons(1.2 * WIDTH, 0.85 * HEIGHT, 0.1 * WIDTH, int(0.1 * HEIGHT), "Restart")

    # Creating all the slider objects
    g_slider = sl.Slider(WIN, 1100, 200, 300, 30, min=0, max=200)
    mass_slider = sl.Slider(WIN, 1100, 400, 300, 30, min=0, max=200)
    g_textbox = tb.TextBox(WIN, 1225, 250, 50, 50, fontSize=30)
    mass_textbox = tb.TextBox(WIN, 1225, 450, 50, 50, fontSize=30)


    # Starting Simulation Loop
    while run:
        # If the simulation has just started, create all the planets
        if start_sim:
            planets = set_planets()
            start_sim = False

        # Setting the frame rate
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # If the music is not playing, play it
        if music == 0:
            pygame.mixer.music.play(-1)
            music = 1

        # Adding the time passed to the time passed variable each frame
        time_passed += Planet.TIMESTEP

        # Drawing the background
        if background_use:
            backgroundimg = pygame.transform.scale(background, (background_w, background_h))
            WIN.blit(backgroundimg, (0, 0))
        else:
            WIN.fill(BLACK)

        # Handling events
        for event in pygame.event.get():

            # If the user clicks the close button, go back to the start menu
            if event.type == pygame.QUIT:
                start_menu()
            elif event.type == pygame.KEYDOWN:
                # If the user presses w or s, change the planet scale to zoom in or out
                if event.key == pygame.K_w:
                    if Planet.SCALE < 2.5e-8:
                        Planet.SCALE *= 1.0005
                        background_w += 50 / WIDTH
                        background_h += 50 / HEIGHT
                elif event.key == pygame.K_s:
                    if Planet.SCALE > 6e-11:
                        Planet.SCALE /= 1.0005
                        background_w -= 50 / WIDTH
                        background_h -= 50 / HEIGHT

                # If the user presses a or d, change the time step to speed up or slow down the simulation
                elif event.key == pygame.K_a and Planet.TIMESTEP != 0:
                    # Only if the simulation isn't paused
                    Planet.TIMESTEP /= 1.0005
                    for k in Planet.planets_points:
                        Planet.planets_points[k] *= 1.0005

                elif event.key == pygame.K_d and Planet.TIMESTEP != 0:
                    Planet.TIMESTEP *= 1.0005
                    for k in Planet.planets_points:
                        Planet.planets_points[k] /= 1.0005

                # if the user presses the arrows keys, move the screen in the correct direction
                elif event.key == pygame.K_RIGHT:
                    Planet.displacement_x -= 1

                elif event.key == pygame.K_LEFT:
                    Planet.displacement_x += 1

                elif event.key == pygame.K_DOWN:
                    Planet.displacement_y -= 1

                elif event.key == pygame.K_UP:
                    Planet.displacement_y += 1

                # If the user presses space, reset the screen to the default position
                elif event.key == pygame.K_SPACE:
                    Planet.displacement_y = 0
                    Planet.displacement_x = 0

                # If the user presses enter, reset the scale to the default value
                elif event.key == pygame.K_RETURN:
                    Planet.SCALE = 250 / Planet.AU

            # If the user clicks the mouse, store the position of the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                temp_mouse_pos = event.pos

                for planet in planets:
                    # Check all planets to see if the user clicked on one
                    if planet.clicked(temp_mouse_pos):
                        # If the user clicked on a planet, open the planet info screen
                        if planet_info == 0:
                            planet_info = 1
                            planet_clicked = planet

                        elif planet_info == 1 and planet == planet_clicked:
                            # If the user clicks on the same planet again, close the planet info screen
                            planet_info = 0

                        else:
                            planet_clicked = planet
                if pause_button.collidepoint(temp_mouse_pos):
                    if settings is False:
                        if Planet.TIMESTEP != 0:
                            temp, Planet.TIMESTEP = Planet.TIMESTEP, 0
                            pause = 1
                        else:
                            Planet.TIMESTEP = temp
                            pause = 0

                elif mute_button.collidepoint(temp_mouse_pos):
                    if settings is False:
                        if music == 1:
                            pygame.mixer.music.pause()
                            mute_button.text = "Unmute"
                            music = 2
                        elif music == 2:
                            mute_button.text = "Mute"
                            music = 0

                elif settings_button.collidepoint(temp_mouse_pos):
                    if settings is False:
                        settings = True
                    else:
                        settings = False

                elif restart_button.collidepoint(temp_mouse_pos):
                    planets = set_planets()

        for planet in planets:

            if planet.clicked(mouse_pos):
                # 1
                planet.hovered = True
            else:
                planet.hovered = False
            planet.update_position(planets)
            planet.draw(WIN)

            if planet.hovered is True:
                x = planet.x * planet.SCALE + WIDTH / 2 + planet.displacement_x
                y = planet.y * planet.SCALE + HEIGHT / 2 + planet.displacement_y
                radius = planet.radius * planet.SCALE * planet.planet_scale + (7 * Planet.SCALE * planet.planet_scale)
                pygame.draw.circle(WIN, planet.color, (x, y), radius, 2)
                pygame.draw.line(WIN, planet.color, (x + radius - 1, y), (x + radius + 40, y), 2)
                display_text(planet.name, x + radius + 42, y - 9, 15, planet.color)

        # Side Window Code
        pygame.draw.rect(WIN, LIGHT_GREY, SIDE_WINDOW)
        control_keys = ["W:", "A:", "S:", "D:", "Up:", "Down:", "Left:", "Right:", "Space:"]
        controls = ["Zoom in", "Slow Down", "Zoom Out", "Speed Up", "Move Up", "Move Down", "Move Left", "Move Right",
                    "Reset Movement"]
        display_text("Controls", 1200, 75, 30, BLACK)
        for i, key in enumerate(control_keys):
            display_text(key, 1150, 150 + (40 * i), 20, BLACK)
        for i, control in enumerate(controls):
            display_text(control, 1275, 150 + (40 * i), 20, BLACK)

        display_text("Variables", 1200, 525, 30, BLACK)
        variables = ["Timescale:", "FPS: ", "Time Passed:", "Current Year:", "Zoom:"]
        for i, variable in enumerate(variables):
            display_text(variable, 1100, 600 + (50 * i), 20, BLACK)
        variable_values = [f"{round(Planet.TIMESTEP / 86400, 2)} Days Per Frame",
                           f"{round(clock.get_fps(), 2)}",
                           f"{round((time_passed / 86400) / 365, 1)} Years Or"
                           f" {int(round((time_passed / 86400), 0))} Days",
                           f"{int(start_year + (round((time_passed / 86400) / 365, 1)))}",
                           f"{round(Planet.SCALE, 12)} Km Per Pixel"
                           ]

        for i, value in enumerate(variable_values):
            display_text(value, 1250, 600 + (50 * i), 20, BLACK)

        # display_text(f"Timescale: {round(Planet.TIMESTEP / 86400, 2)} Days Per Frame", 1.1 * WIDTH, 0.6 * HEIGHT,
        # int(0.02 * HEIGHT), BLACK)
        # display_text(f"FPS: {round(clock.get_fps(), 2)}", 1.15 * WIDTH, 0.7 * HEIGHT, int(0.02 * HEIGHT), WHITE)
        # display_text(f"Time Passed: {round((time_passed / 86400) / 365, 1)} Years Or"
        # f" {int(round((time_passed / 86400), 0))} Days", 1.15 * WIDTH, 0.8 * HEIGHT, int(0.02 * HEIGHT),
        # WHITE)

        if pause == 0:
            pause_button.draw("assets/gfx/pause.png", WIN)
        else:
            pause_button.draw("assets/gfx/play_sim.png", WIN)

        if music == 1:
            mute_button.draw("assets/gfx/volume.png", WIN)
        else:
            mute_button.draw("assets/gfx/mute.png", WIN)

        if settings is True:
            pygame.draw.rect(WIN, LIGHT_GREY, [1000, 0, 500, 1000])
            display_text("Settings", 1190, 10, 40, BLACK)
            display_text("G Value", 1200, 150, 30, BLACK)
            g_textbox.setText(g_slider.getValue())
            display_text("Mass Multiplier", 1155, 350, 30, BLACK)
            mass_textbox.setText(mass_slider.getValue())

        restart_button.draw("assets/gfx/repeat.png", WIN)

        settings_button.draw("assets/gfx/settings_sim.png", WIN)

        # ok
        # ffffffffffffff
        if planet_info == 1:
            pygame.draw.rect(WIN, LIGHT_GREY, [1000, 0, 500, 1000])
            display_text(planet_clicked.name, 1250 - (8 * len(planet_clicked.name)), 10, 40, BLACK)
            planet_image = pygame.image.load(f"assets/gfx/{planet_clicked.name}_real.png").convert_alpha()
            planet_image = pygame.transform.scale(planet_image, (150, 150))
            shadow = pygame.image.load("assets/gfx/shadow.png").convert_alpha()
            shadow = pygame.transform.scale(shadow, (150, 150))
            WIN.blit(shadow, (1185, 120))
            WIN.blit(planet_image, (1185, 100))
            fact_file = open(f"data/info/{planet_clicked.name}.txt", "rb")
            fact_info = fact_file.readlines()
            if planet_clicked.name!= "Sun":
                facts = ["Mass", "Radius", "Escape Velocity", "Mean Orbital Velocity",
                         "Volume", "Surface Gravity", "Mean Density", "Distance From Sun"]
                fact_info.append(f"{str(round(planet_clicked.distance_to_sun / 100000000, 0) * 100000)} km..")
            else:
                facts = ["Mass", "Radius", "Escape Velocity", "Mean Orbital Velocity",
                         "Volume", "Surface Gravity", "Mean Density", "Luminosity"]

            for i, fact in enumerate(facts):
                display_text(fact, 1100, 300 + (60 * i), 20, BLACK)

            # ffffffff
            for i, info in enumerate(fact_info):
                display_text(info[:-2], 1300, 300 + (60 * i), 20, BLACK)

        if settings:
            event = pygame.event.get()
            pw.update(event)
            Planet.g_scale = g_slider.getValue() / 100
            Planet.mass_multiplier = mass_slider.getValue() / 100

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

else:
    print("Simulation loaded")

# To add
# Faster = fewer points, DONE
# Pause, DONE
# Settings, DONE
# Music, DONE
# Other systems
#
