import numpy as np
import os
from pathlib import Path
import pygame
import pygame_widgets
import random
import time
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


# ********************************** Variables ******************************************
SCREEN_HIGH = 800
SCREEN_WIDTH = 1320
ARRAY_GREY = [128, 128, 128]
ARRAY_CLEAR_GREY = [228, 228, 228]
ARRAY_WHITE = [255, 255, 255]
ARRAY_BLACK = [0, 0, 0]
TABLE_HIGH = 25
TABLE_WIDTH = 40
IMAGES_VALUE = {0: "fire", 1: "vide", 2: "rock", 3: "tree"}
PATH_TO_IMAGES = Path("static/imgs")
wind = 0

# Générer aléatoirement une nouvelle forêt
def create_screen():
    pygame.init()
    pygame.display.set_caption("Simulation de feux de forêts")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGH))
    reset_screen(screen)
    pygame.display.flip()
    return screen


def reset_screen(screen):
    screen.fill(ARRAY_WHITE)
    pygame.draw.rect(screen, ARRAY_GREY, pygame.Rect(50, 50, 1000, 625), 1)
    pygame.draw.rect(screen, ARRAY_CLEAR_GREY, pygame.Rect(1090, 50, 200, 625), 0)


def generate_forest(rocks_percentage=0, trees_percentage=1, fires_percentage=0):
    return np.random.choice([0, 2, 3], size=(TABLE_HIGH, TABLE_WIDTH), p=[fires_percentage,
                                                                          rocks_percentage,
                                                                          trees_percentage])


def display_forest(images):
    reset_screen(screen)
    # pygame.display.flip()
    for line in range(TABLE_HIGH):
        for column in range(TABLE_WIDTH):
            if table[line, column] != 2:
                picture = images[IMAGES_VALUE[table[line, column]]][0]
                screen.blit(picture, (50 + column * 25, 50 + line * 25))


def generate_next_generation(est_wind=False):
    global table
    global wind
    global generating
    stop_generations = False
    temporary_table = table.copy()
    for line in range(1, TABLE_HIGH - 1):
        for column in range(1, TABLE_WIDTH - 1):
            if table[line, column] == 0:
                temporary_table[line, column] = 1
            if not wind and table[line, column] == 3:
                if table[line - 1, column - 1] == 0 or table[line - 1, column] == 0 or \
                        table[line - 1, column + 1] == 0 or table[line, column - 1] == 0 or \
                        table[line, column + 1] == 0 or table[line + 1, column - 1] == 0 or \
                        table[line + 1, column] == 0 or table[line + 1, column + 1] == 0:
                    temporary_table[line, column] = 0
                    if not stop_generations:
                        stop_generations = True
            else:
                if table[line, column] == 3 and (table[line + 1, column - 1] == 0 or
                                                 table[line + 1, column] == 0 or
                                                 table[line + 1, column + 1] == 0):
                    temporary_table[line, column] = 0
                    if not stop_generations:
                        stop_generations = True
    del(table)
    generating = stop_generations
    table = temporary_table
    return table


def load_images():
    images_dict = dict()
    for directory in os.listdir(Path(PATH_TO_IMAGES)):
        # print(directory)
        images_dict[directory] = list()
        for image in os.listdir(Path(PATH_TO_IMAGES / directory)):
            path_to_picture = Path(PATH_TO_IMAGES / directory / image).absolute().as_posix()
            picture = pygame.image.load(path_to_picture)
            if directory == "wind":
                picture_transformed = pygame.transform.scale(picture, (100, 100))
            else:
                picture_transformed = pygame.transform.scale(picture, (25, 25))
            images_dict[directory].append(picture_transformed)
    return images_dict


def generate_new_forest_button():
    global table
    global images
    table = generate_forest(trees_percentage=slider_trees.getValue()/100,
                            fires_percentage=slider_fires.getValue()/100,
                            rocks_percentage=slider_vides.getValue()/100)
    display_forest(images)


def create_buttons(screen):
    Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        1100,  # X-coordinate of top left corner
        280,  # Y-coordinate of top left corner
        180,  # Width
        50,  # Height

        # Optional Parameters
        text='Générate Random Forest',  # Text to display
        fontSize=20,  # Size of font
        margin=10,  # Minimum distance between text/image and edge of button
        inactiveColour=(200, 255, 200),  # Colour of button when not being interacted with
        hoverColour=(250, 250, 250),  # Colour of button when being hovered over
        pressedColour=(10, 255, 10),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: generate_new_forest_button()  # Function to call when clicked on
    )


def create_slider_trees(screen):
    label = TextBox(win=screen, x=1165, y=85, width=100, height=20, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    label.disable()
    label.setText("Arbres")
    value = TextBox(win=screen, x=1165, y=100, width=100, height=25, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    value.disable()
    slider = Slider(win=screen, x=1115, y=120, width=150, height=10, min=0, max=100, step=0.01, colour=[0, 0, 0],
                  handleColour=ARRAY_CLEAR_GREY)
    slider.setValue(100)
    return slider, value


def create_slider_vides(screen):
    label = TextBox(win=screen, x=1165, y=145, width=100, height=20, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    label.disable()
    label.setText("Vides")
    value = TextBox(win=screen, x=1165, y=160, width=100, height=25, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    value.disable()
    slider = Slider(win=screen, x=1115, y=180, width=150, height=10, min=0, max=100, step=0.01, colour=[0, 0, 0],
                  handleColour=ARRAY_CLEAR_GREY)
    return slider, value


def create_slider_fires(screen):
    label = TextBox(win=screen, x=1165, y=205, width=100, height=20, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    label.disable()
    label.setText("Feux")
    value = TextBox(win=screen, x=1165, y=220, width=100, height=25, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    value.disable()
    slider = Slider(win=screen, x=1115, y=240, width=150, height=10, min=0, max=100, step=0.01, colour=[0, 0, 0],
                  handleColour=ARRAY_CLEAR_GREY)
    return slider, value


def create_slider_speed(screen):
    label = TextBox(win=screen, x=1165, y=425, width=100, height=20, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    label.disable()
    label.setText("Vitesse")
    value = TextBox(win=screen, x=1165, y=440, width=100, height=25, fontSize=20, colour=ARRAY_CLEAR_GREY, textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
    value.disable()
    slider = Slider(win=screen, x=1115, y=460, width=150, height=10, min=1, max=50, step=1, colour=[0, 0, 0],
                  handleColour=ARRAY_CLEAR_GREY)
    slider.setValue(5)
    return slider, value


def change_cell(x, y):
    global table
    global images
    table[y, x] = (table[y, x] + 1) % 4
    display_forest(images)


def show_wind_button():
    global wind
    global wind_button
    if wind == 1:
        wind_button.text = wind_button.font.render("Cliquer ici pour activer le vent", True, wind_button.textColour)
        wind_button.setImage(images['wind'][1])
        wind = 0
    else:
        wind_button.text = wind_button.font.render("", True, wind_button.textColour)
        wind_button.setImage(images['wind'][0])
        wind = 1


def create_buttons_wind(screen):
    return Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        50,  # X-coordinate of top left corner
        680,  # Y-coordinate of top left corner
        1000,  # Width
        100,  # Height
        text="Cliquer ici pour activer le vent",
        inactiveColour=(255, 255, 255),  # Colour of button when not being interacted with
        hoverColour=(240, 240, 240),  # Colour of button when being hovered over
        pressedColour=(240, 255, 240),  # Colour of button when being clicked
        onClick=lambda: show_wind_button()  # Function to call when clicked on
    )


table = generate_forest()
images = load_images()

screen = create_screen()
slider_trees, slider_trees_value = create_slider_trees(screen)
slider_vides, slider_vides_value = create_slider_vides(screen)
slider_fires, slider_fires_value = create_slider_fires(screen)
slider_speed, slider_speed_value = create_slider_speed(screen)
wind_button = create_buttons_wind(screen)

nb_generations = 0
generating = False

nb_of_generations = TextBox(win=screen, x=1165, y=645, width=100, height=20, fontSize=20, colour=ARRAY_CLEAR_GREY,
                    textColour=ARRAY_BLACK, borderColour=ARRAY_CLEAR_GREY)
nb_of_generations.setText("test")


def launch():
    global nb_generations
    global generating
    nb_generations = 0
    generating = True


def stop():
    global nb_generations
    global generating
    nb_generations = 0
    generating = False


Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    1100,  # X-coordinate of top left corner
    520,  # Y-coordinate of top left corner
    180,  # Width
    50,  # Height
    # Optional Parameters
    text='Lancer',  # Text to display
    fontSize=20,  # Size of font
    margin=10,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 255, 200),  # Colour of button when not being interacted with
    hoverColour=(250, 250, 250),  # Colour of button when being hovered over
    pressedColour=(10, 255, 10),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: launch()  # Function to call when clicked on
)

Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    1100,  # X-coordinate of top left corner
    580,  # Y-coordinate of top left corner
    180,  # Width
    50,  # Height
    # Optional Parameters
    text='Arrêter',  # Text to display
    fontSize=20,  # Size of font
    margin=10,  # Minimum distance between text/image and edge of button
    inactiveColour=(255, 200, 200),  # Colour of button when not being interacted with
    hoverColour=(250, 250, 250),  # Colour of button when being hovered over
    pressedColour=(10, 255, 10),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: stop()  # Function to call when clicked on
)


if __name__ == "__main__":
    create_buttons(screen)
    display_forest(images)

    launched = True
    clock = pygame.time.Clock()
    while launched:
        for event in pygame.event.get():
            # print(event)
            # Quitter
            if event.type == pygame.QUIT:
                launched = False
            # Changer le type d'une cellule
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if (mouse_position[0] - 50) < 0 or (mouse_position[1] - 50) < 0 or \
                        (mouse_position[0] - 50) > 1000 or (mouse_position[1] - 50) > 625:
                    continue
                print((mouse_position[0] - 50) // 25, (mouse_position[1] - 50) // 25)
                change_cell((mouse_position[0] - 50) // 25, (mouse_position[1] - 50) // 25)
        pygame.display.flip()
        pygame_widgets.update(event)
        pygame.display.update()
        slider_vides.setValue(max(0, 100 - (slider_trees.getValue() + slider_fires.getValue())))
        if slider_trees.getValue() + slider_fires.getValue() > 100:
            slider_fires.setValue(100 - (slider_vides.getValue() + slider_trees.getValue()))

        slider_speed_value.setText(slider_speed.getValue())

        slider_trees_value.setText(str(round(slider_trees.getValue(), 2)) + " %")
        slider_fires_value.setText(str(round(slider_fires.getValue(), 2)) + " %")
        slider_vides_value.setText(str(round(slider_vides.getValue(), 2)) + " %")
        clock.tick(slider_speed.getValue())
        if generating:
            nb_of_generations.setText(nb_generations)
            generate_next_generation()
            display_forest(images)
            pygame.display.update()
            nb_generations += 1
