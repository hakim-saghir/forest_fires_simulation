import pygame_widgets
from config import COLOR_LIGHT_GREY, COLOR_BLACK
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


# ######################################## CREATION DES WIDGETS ################################################### #
#####################################################################################################################


####################################################################################################################
# ################################################ SLIDERS ####################################################### #
####################################################################################################################
class ControlsSlidersClass:

    def __init__(self, model_arg):
        self.model = model_arg
        # ****************** Slider du pourcentage d'arbres ********************
        self.slider_trees_percentage = Slider(win=self.model.screen, x=1115, y=120, width=150, height=10, min=0, max=100,
                                              step=0.01, colour=[0, 0, 0], handleColour=COLOR_LIGHT_GREY)
        self.slider_trees_percentage.setValue(60)
        # *************** Slider du pourcentage des vides **********************
        self.slider_empty_percentage = Slider(win=self.model.screen, x=1115, y=180, width=150, height=10, min=0, max=100,
                                              step=0.01, colour=[0, 0, 0], handleColour=COLOR_LIGHT_GREY)
        self.slider_empty_percentage.setValue(40)
        # ***************** Slider du pourcentage des feux *********************
        self.slider_fires_percentage = Slider(win=self.model.screen, x=1115, y=240, width=150, height=10, min=0, max=100,
                                              step=0.01, colour=[0, 0, 0], handleColour=COLOR_LIGHT_GREY)
        self.slider_fires_percentage.setValue(0)
        # ************************ Slider de la vitesse ************************
        self.slider_speed_percentage = Slider(win=self.model.screen, x=1115, y=460, width=150, height=10, min=1, max=50,
                                              step=1, colour=[0, 0, 0], handleColour=COLOR_LIGHT_GREY)
        self.slider_speed_percentage.setValue(3)

    # Ajuster la valeur des sliders pour avoir toujours une somme des valeurs à 100 %
    def check_sliders_values(self):
        self.slider_empty_percentage.setValue(max(0, 100 - self.slider_trees_percentage.getValue() -
                                                  self.slider_fires_percentage.getValue()))
        if (self.slider_trees_percentage.getValue() + self.slider_fires_percentage.getValue()) > 100:
            self.slider_fires_percentage.setValue(100 - self.slider_empty_percentage.getValue() -
                                                  self.slider_trees_percentage.getValue())


####################################################################################################################
# ################################################ TEXTBOXES ##################################################### #
####################################################################################################################
class ControlsTextBoxesClass:
    def __init__(self, model_arg):
        self.model = model_arg
        # ****************** Slider du pourcentage d'arbres ********************
        # Libéllé
        label = TextBox(win=self.model.screen, x=1165, y=85, width=100, height=20, fontSize=20, colour=COLOR_LIGHT_GREY,
                        textColour=COLOR_BLACK, borderColour=COLOR_LIGHT_GREY)
        label.disable()
        label.setText("Arbres")
        del label
        # Valeur à afficher
        self.display_trees_percentage = TextBox(win=self.model.screen, x=1165, y=100, width=100, height=20, fontSize=20,
                                                colour=COLOR_LIGHT_GREY, textColour=COLOR_BLACK,
                                                borderColour=COLOR_LIGHT_GREY)
        self.display_trees_percentage.disable()
        # *************** Slider du pourcentage des vides **********************
        # Libéllé
        label = TextBox(win=self.model.screen, x=1165, y=145, width=100, height=20, fontSize=20, colour=COLOR_LIGHT_GREY,
                        textColour=COLOR_BLACK, borderColour=COLOR_LIGHT_GREY)
        label.disable()
        label.setText("Vides")
        # Valeur à afficher
        self.display_empty_percentage = TextBox(win=self.model.screen, x=1165, y=160, width=100, height=20, fontSize=20,
                                                colour=COLOR_LIGHT_GREY, textColour=COLOR_BLACK,
                                                borderColour=COLOR_LIGHT_GREY)
        self.display_empty_percentage.disable()
        # ***************** Slider du pourcentage des feux *********************
        # Libéllé
        label = TextBox(win=self.model.screen, x=1165, y=205, width=100, height=20, fontSize=20, colour=COLOR_LIGHT_GREY,
                        textColour=COLOR_BLACK, borderColour=COLOR_LIGHT_GREY)
        label.disable()
        label.setText("Feux")
        del label
        # Valeur à afficher
        self.display_fires_percentage = TextBox(win=self.model.screen, x=1165, y=220, width=100, height=20, fontSize=20,
                                                colour=COLOR_LIGHT_GREY, textColour=COLOR_BLACK,
                                                borderColour=COLOR_LIGHT_GREY)
        self.display_fires_percentage.disable()
        # ************************ Slider de la vitesse ************************
        # Libéllé
        label = TextBox(win=self.model.screen, x=1165, y=425, width=100, height=20, fontSize=20, colour=COLOR_LIGHT_GREY,
                        textColour=COLOR_BLACK, borderColour=COLOR_LIGHT_GREY)
        label.disable()
        label.setText("Vitesse")
        del label
        # Valeur à afficher
        self.display_speed_percentage = TextBox(win=self.model.screen, x=1165, y=440, width=100, height=20, fontSize=20,
                                                colour=COLOR_LIGHT_GREY, textColour=COLOR_BLACK,
                                                borderColour=COLOR_LIGHT_GREY)
        self.display_speed_percentage.disable()

        # ******************* Affichage du nombre de générations ***************
        self.current_generation = TextBox(win=self.model.screen, x=1165, y=645, width=100, height=20, fontSize=20,
                                          colour=COLOR_LIGHT_GREY,
                                          textColour=COLOR_BLACK, borderColour=COLOR_LIGHT_GREY)

    # Mettre à jour la valeur des sliders
    def update_sliders_display(self):
        self.display_trees_percentage.setText(str(round(self.model.sliders.slider_trees_percentage.getValue(), 2))+" %")
        self.display_empty_percentage.setText(str(round(self.model.sliders.slider_empty_percentage.getValue(), 2))+" %")
        self.display_fires_percentage.setText(str(round(self.model.sliders.slider_fires_percentage.getValue(), 2))+" %")
        self.display_speed_percentage.setText(self.model.sliders.slider_speed_percentage.getValue())

    # Mettre à jour le numéro de la génération
    def update_current_generation_display(self, current_generation):
        self.current_generation.setText(current_generation)


####################################################################################################################
# ################################################ BOUTTONS ###################################################### #
####################################################################################################################
class ControlsButtonsClass:
    # ** Mandatory Parameters **
    # Surface to place button on
    # X-coordinate of top left corner
    # Y-coordinate of top left corner
    # Width
    # Height
    # ** Optional Parameters **
    # text : Text to display
    # fontSize : Size of font
    # margin : Minimum distance between text/image and edge of button
    # inactiveColour : Colour of button when not being interacted with
    # hoverColour :  Colour of button when being hovered over
    # pressedColour : Colour of button when being clicked
    # radius : Radius of border corners (leave empty for not curved)
    # onClick : Function to call when clicked on

    def __init__(self, model_arg):
        self.model = model_arg
        self.WIND_SOUTH_ENABLED = False
        self.GENERATION_LAUNCHED = False
        self.AUTO_REGENERATE_FOREST = False
        self.CURRENT_GENERATION = 0

        # *** Boutton de génération de forêt
        self.button_generate = Button(self.model.screen, 1100, 280, 180, 50, text="Générer une forêt random", fontSize=20,
                                      margin=10, inactiveColour=(200, 255, 200), hoverColour=(250, 250, 250),
                                      pressedColour=(10, 255, 10), radius=20,
                                      onClick=lambda: self.generate_new_forest_button())

        # *** Boutton de lancement de génération
        self.button_launch = Button(self.model.screen, 1100, 520, 180, 50, text="Lancer", fontSize=20, margin=10,
                                    inactiveColour=(200, 255, 200), hoverColour=(250, 250, 250),
                                    pressedColour=(10, 255, 10), radius=20, onClick=lambda: self.launch_generation())

        # *** Boutton d'arrêt de la génération
        self.button_stop = Button(self.model.screen, 1100, 580, 180, 50, text="Arrêter", fontSize=20, margin=10,
                                  inactiveColour=(255, 200, 200), hoverColour=(250, 250, 250),
                                  pressedColour=(10, 255, 10), radius=20, onClick=lambda: self.stop_generation())

        # *** Boutton d'arrêt de la génération
        self.button_wind_south = Button(self.model.screen, 50, 680, 1000, 100, text="Cliquer ici pour activer le vent",
                                        inactiveColour=(255, 255, 255), hoverColour=(240, 240, 240),
                                        pressedColour=(240, 240, 240), radius=20, onClick=lambda: self.show_wind_button())

        # *** Boutton d'arrêt de la génération
        self.auto_regenerate = Button(self.model.screen, 1100, 350, 180, 30, text="Regénérer après 200 gen",
                                      inactiveColour=(255, 0, 0),
                                      pressedColour=(240, 240, 240), radius=20,
                                      onClick=lambda: self.auto_regenerate_button())

    def auto_regenerate_button(self):
        if self.AUTO_REGENERATE_FOREST:
            self.auto_regenerate.setInactiveColour((255, 0, 0))
            self.AUTO_REGENERATE_FOREST = False
        else:
            self.auto_regenerate.setInactiveColour((0, 255, 0))
            self.AUTO_REGENERATE_FOREST = True

        pygame_widgets.update(None)

    def generate_new_forest_button(self):
        self.model.generate_random_forest_matrix(self.model.sliders.slider_trees_percentage.getValue() / 100,
                                                 self.model.sliders.slider_empty_percentage.getValue() / 100,
                                                 self.model.sliders.slider_fires_percentage.getValue() / 100)
        self.model.display_matrix()

    def show_wind_button(self):
        if self.WIND_SOUTH_ENABLED == 1:
            self.button_wind_south.text = self.button_wind_south.font.render("Cliquer ici pour activer le vent",
                                                                             True,
                                                                             self.button_wind_south.textColour)
            self.button_wind_south.setImage(self.model.images_array['wind'][1])
            self.WIND_SOUTH_ENABLED = 0
        else:
            self.button_wind_south.text = self.button_wind_south.font.render("", True, self.button_wind_south.textColour)
            self.button_wind_south.setImage(self.model.images_array['wind'][0])
            self.WIND_SOUTH_ENABLED = 1

    def launch_generation(self):
        self.CURRENT_GENERATION = 0
        self.GENERATION_LAUNCHED = True
        self.model.textboxes.update_current_generation_display(self.CURRENT_GENERATION)

    def stop_generation(self):
        self.GENERATION_LAUNCHED = False

    def increment_generation(self):
        self.CURRENT_GENERATION += 1
        self.model.textboxes.update_current_generation_display(self.CURRENT_GENERATION)
