from pathlib import Path

# CONFIGURATION DE l'ECRAN
SCREEN_HIGH = 800
SCREEN_WIDTH = 1320
SCREEN_RIGHT_PADDING = 50
SCREEN_LEFT_PADDING = 50
SCREEN_BOTTOM_PADDING = 50
SCREEN_TOP_PADDING = 50

# COULEURS
COLOR_GREY = [128, 128, 128]
COLOR_LIGHT_GREY = [228, 228, 228]
COLOR_WHITE = [255, 255, 255]
COLOR_BLACK = [0, 0, 0]

# TAILLES DE LA MATRICE
TABLE_HIGH = 27
TABLE_WIDTH = 42

# IMAGES
IMAGES_PATH = Path("static/imgs")
PATH_TO_LOGO = "./static/forest-fire-logo.png"
IMAGES_VALUE = {0: "fire",
                1: "vide",
                3: "tree"}
IMAGE_WIDTH = 25
IMAGE_HEIGHT = 25
WIND_IMAGE_WIDTH = 100
WIND_IMAGE_HEIGHT = 100

# AUTRES TAILLES
FOREST_CONTOUR_WIDTH = (TABLE_WIDTH - 2) * IMAGE_WIDTH
FOREST_CONTOUR_HEIGHT = (TABLE_HIGH - 2) * IMAGE_HEIGHT
PARAMETERS_CONTOUR_WIDTH = 200
PARAMETERS_CONTOUR_HEIGHT = FOREST_CONTOUR_HEIGHT
PARAMETERS_X_START = 1090

# CONFIGURATION DE LA SIMULATION
WIND_SOUTH_ENABLED = False
STOP_IF_NO_FIRE = False
AUTO_REGENERATE_FOREST_AFTER_GENERATIONS = 200
