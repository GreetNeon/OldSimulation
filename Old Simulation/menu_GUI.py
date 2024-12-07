import pygame
import sys
from run_GUI import start_sim
from simulation_classes import Buttons
import PygameUtils as pu
from pickle_editor import load, save

pygame.init()
WIDTH, HEIGHT = 1500, 1000
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("assets/gfx/menu_background.png"), (WIDTH, HEIGHT))


def get_font(size):
    return pygame.font.Font("assets/font/impact.ttf", size)

def display_text(text, x, y, size, colour):
    font = pygame.font.Font('assets/font/impact.ttf', size)
    message = font.render(text, True, colour)
    main_screen.blit(message, (x, y))

def play():
    start_sim()


def options():

    back_button = Buttons(10, 10, 100, 50, "Back")
    save_button = Buttons(700, 800, 100, 50, "Save")
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        main_screen.fill("white")

        if not back_button.collidepoint(options_mouse_pos):
            display_text(back_button.text, 10, 10, 40, "#000000")
        else:
            display_text(back_button.text, 10, 10, 40, "#7dff00")

        if not save_button.collidepoint(options_mouse_pos):
            display_text(save_button.text, 700, 800, 40, "#000000")
        else:
            display_text(save_button.text, 700, 800, 40, "#7dff00")


        display_text("SETTINGS", 510, 20, 140, "#b68f40")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def main_menu():
    while True:
        main_screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        display_text("MAIN MENU", 430, 20, 140, "#b68f40")

        play_button = Buttons(620, 270, 300, 140, "Play")
        if not play_button.collidepoint(menu_mouse_pos):
            display_text(play_button.text, 640, 270, 100, "#ffffff")
        else:
            display_text(play_button.text, 640, 270, 100, "#7dff00")


        settings_button = Buttons(530, 460, 500, 140, "Settings")
        if not settings_button.collidepoint(menu_mouse_pos):
            display_text(settings_button.text, 550, 460, 100, "#ffffff")
        else:
            display_text(settings_button.text, 550, 460, 100, "#7dff00")

        exit_button = Buttons(620, 650, 300, 140, "Exit")
        if not exit_button.collidepoint(menu_mouse_pos):
            display_text(exit_button.text, 640, 650, 100, "#ffffff")
        else:
            display_text(exit_button.text, 640, 650, 100, "#7dff00")


        #exit_button = Button(image=pygame.image.load("assets/gfx/exit.png"), pos=(640, 550),
                             #text_input=None, font=get_font(75), base_color="#d7fcd4", hovering_color="White",
                             #button_size=(300, 130))

        #main_screen.blit(menu_text, menu_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                temp_pos = event.pos
                if play_button.collidepoint(temp_pos):
                    play()
                if settings_button.collidepoint(temp_pos):
                    options()
                if exit_button.collidepoint(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
