import numpy as np
import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HIGH, COLOR_WHITE, SCREEN_LEFT_PADDING, SCREEN_TOP_PADDING, \
    FOREST_CONTOUR_WIDTH, FOREST_CONTOUR_HEIGHT, COLOR_GREY, COLOR_LIGHT_GREY, PARAMETERS_X_START, \
    PARAMETERS_CONTOUR_WIDTH, PARAMETERS_CONTOUR_HEIGHT, IMAGES_PATH, TABLE_HIGH, TABLE_WIDTH, IMAGES_VALUE, \
    IMAGE_HEIGHT, IMAGE_WIDTH, WIND_IMAGE_WIDTH, WIND_IMAGE_HEIGHT, PATH_TO_LOGO, STOP_IF_NO_FIRE, \
    AUTO_REGENERATE_FOREST_AFTER_GENERATIONS
from pathlib import Path
from widgets import ControlsSlidersClass, ControlsButtonsClass, ControlsTextBoxesClass


# CREER UN ECRAN
def create_screen():
    pygame.init()
    pygame.display.set_caption("Simulation de feux de forêts")
    pygame.display.set_icon(pygame.image.load(Path(PATH_TO_LOGO)))
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGH))


# CHARGER LES IMAGES ET LES STOCKER DANS UN DICTIONNAIRE
def load_images():
    images_dict = dict()
    for directory in os.listdir(Path(IMAGES_PATH)):
        images_dict[directory] = list()
        for image in os.listdir(Path(IMAGES_PATH / directory)):
            picture = pygame.image.load(Path(IMAGES_PATH / directory / image).absolute().as_posix())
            if directory == "wind":
                picture_transformed = pygame.transform.scale(picture, (WIND_IMAGE_WIDTH, WIND_IMAGE_HEIGHT))
            else:
                picture_transformed = pygame.transform.scale(picture, (IMAGE_WIDTH, IMAGE_HEIGHT))
            images_dict[directory].append(picture_transformed)
    return images_dict


class Model:

    def __init__(self):

        # CREATION ET RENITIALISATION DE L'ECRAN
        self.screen = create_screen()
        self.reset_screen(all=True)

        # RECUPERATION DES IMAGES
        self.images_array = load_images()

        # GENERATION DE LA MATRICE
        self.matrix = None
        self.matrix_generation = np.zeros(shape=(TABLE_HIGH - 2, TABLE_WIDTH - 2), dtype=np.int)

        # CREATION DES SLIDERS ET DES BOUTTONS
        self.sliders = ControlsSlidersClass(self)
        self.textboxes = ControlsTextBoxesClass(self)
        self.buttons = ControlsButtonsClass(self)
        self.buttons.generate_new_forest_button()

    # VIDER L'ECRAN
    def reset_screen(self, all):
        self.screen.fill(COLOR_WHITE)
        pygame.draw.rect(self.screen, COLOR_LIGHT_GREY, pygame.Rect(PARAMETERS_X_START, SCREEN_TOP_PADDING,
                                                                    PARAMETERS_CONTOUR_WIDTH,
                                                                    PARAMETERS_CONTOUR_HEIGHT), 0)
        pygame.draw.rect(self.screen, COLOR_GREY, pygame.Rect(SCREEN_LEFT_PADDING, SCREEN_TOP_PADDING,
                                                              FOREST_CONTOUR_WIDTH, FOREST_CONTOUR_HEIGHT), 1)

    # GENERER UNE MATRICE ALEATOIREMENT (EN FONCTION DES PROBABILITES DE DISRIBUTION CHOISIES)
    def _generate_first_random_forest_matrix(self, trees_percentage=1, empty_percentage=0, fires_percentage=0):
        table = np.random.choice([0, 2, 3], size=(TABLE_HIGH, TABLE_WIDTH), p=[fires_percentage,
                                                                               empty_percentage,
                                                                               trees_percentage])
        for line in range(TABLE_HIGH):
            for column in range(TABLE_WIDTH):
                if line == 0 or column == 0 or \
                        line == TABLE_HIGH - 1 or column == TABLE_WIDTH - 1:
                    table[line, column] = 3
        return table

    def generate_random_forest_matrix(self, trees_percentage=1, empty_percentage=0, fires_percentage=0):
        del self.matrix
        self.matrix = self._generate_first_random_forest_matrix(trees_percentage, empty_percentage, fires_percentage)
        self.display_matrix()

    # AFFICHER L'IMAGE CORRESPONDANT A CHAQUE CELLULE DE LA MATRICE
    def display_matrix(self):
        self.reset_screen(all=False)
        for line in range(1, TABLE_HIGH - 1):
            for column in range(1, TABLE_WIDTH - 1):
                if self.matrix[line, column] != 2:
                    picture = self.images_array[IMAGES_VALUE[self.matrix[line, column]]][0]
                    self.screen.blit(picture, (SCREEN_LEFT_PADDING + (column - 1) * IMAGE_WIDTH,
                                               SCREEN_TOP_PADDING + (line - 1) * IMAGE_HEIGHT))
                    del picture

    # INCREMENTER UNE CELLULE DE LA MATRICE
    def change_cell(self, x, y):
        self.matrix[y, x] = (self.matrix[y, x] + 1) % 4
        if self.buttons.AUTO_REGENERATE_FOREST and self.matrix[y, x] == 1:
            self.matrix_generation[y - 1, x - 1] = 0
        self.display_matrix()

    # GENERER LA GENERATION SUIVANTE DE LA MATRICE
    def generate_matrix_next_generation(self, wind_south):
        temporary_matrix = self.matrix.copy()
        stop_generations = True
        for line in range(1, TABLE_HIGH - 1):
            for column in range(1, TABLE_WIDTH - 1):
                # Vide
                if self.buttons.AUTO_REGENERATE_FOREST and self.matrix[line, column] == 1:
                    self.matrix_generation[line - 1, column - 1] += 1
                    if self.matrix_generation[line - 1, column - 1] == AUTO_REGENERATE_FOREST_AFTER_GENERATIONS:
                        temporary_matrix[line, column] = 3
                    # Feu
                elif self.matrix[line, column] == 0:
                    temporary_matrix[line, column] = 1
                    self.matrix_generation[line - 1, column - 1] = 0
                # Arbre
                elif self.matrix[line, column] == 3 and \
                        ((not wind_south and (not self.matrix[line - 1, column - 1] or
                                              not self.matrix[line - 1, column] or
                                              not self.matrix[line - 1, column + 1] or
                                              not self.matrix[line, column - 1] or
                                              not self.matrix[line, column + 1] or
                                              not self.matrix[line + 1, column - 1] or
                                              not self.matrix[line + 1, column] or
                                              not self.matrix[line + 1, column + 1]))
                         or (wind_south and (not self.matrix[line + 1, column - 1] or
                                             not self.matrix[line + 1, column] or
                                             not self.matrix[line + 1, column + 1]))):
                    temporary_matrix[line, column] = 0
                    stop_generations = False
        if stop_generations and STOP_IF_NO_FIRE:
            self.buttons.stop_generation()
        del self.matrix
        self.matrix = temporary_matrix.copy()
        del temporary_matrix
        self.display_matrix()
