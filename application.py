import pygame
import pygame_widgets

from config import SCREEN_LEFT_PADDING, SCREEN_TOP_PADDING, TABLE_WIDTH, IMAGE_WIDTH, IMAGE_HEIGHT, TABLE_HIGH
from model import Model

if __name__ == "__main__":
    model = Model()
    model.display_matrix()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():

            # Boutton quitter
            if event.type == pygame.QUIT:
                running = False
                break

            # Clic dans la forêt
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_position = pygame.mouse.get_pos()
                if (mouse_position[0] - SCREEN_LEFT_PADDING) < 0 or (mouse_position[1] - SCREEN_TOP_PADDING) < 0 or \
                        (mouse_position[0] - SCREEN_LEFT_PADDING) > ((TABLE_WIDTH - 2) * IMAGE_WIDTH) \
                        or (mouse_position[1] - SCREEN_TOP_PADDING) > ((TABLE_HIGH - 2) * IMAGE_HEIGHT):
                    continue
                model.change_cell(((mouse_position[0] - SCREEN_LEFT_PADDING) // IMAGE_WIDTH) + 1,
                                  ((mouse_position[1] - SCREEN_TOP_PADDING) // IMAGE_HEIGHT) + 1)

            # Modification des valeurs des sliders
            if event.type == pygame.MOUSEMOTION:
                model.sliders.check_sliders_values()
                model.textboxes.update_sliders_display()

        if model.buttons.GENERATION_LAUNCHED:
            model.generate_matrix_next_generation(model.buttons.WIND_SOUTH_ENABLED)
            model.buttons.increment_generation()

        pygame_widgets.update(None)
        pygame.display.update()
        clock.tick(model.sliders.slider_speed_percentage.getValue())
