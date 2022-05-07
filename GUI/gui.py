from time import sleep

import arcade
import numpy as np
from PIL import Image

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 50

#TODO uzyc center_window()
class GUI(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, path):
        """
        Set up the application.
        """
        # TODO zapisac mapke, bedzie sie szybciej uruchamiac

        self.map = self._convert_to_binary_map(path)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        super().__init__(self.y_size, self.x_size + 100,
                         SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        self.day = 0
        self.text = f"Day: {self.day}"
        # Set the window's background color
        self.background_color = arcade.color.WHITE
        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()
        self.initialize_grid()
        arcade.schedule(self.update_day, 1)

    def update_day(self, delta_time):
        self.day += 1
        self.text = f"Day: {self.day}"

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()
        arcade.draw_text(self.text, TEXT_PADDING, self.x_size + TEXT_PADDING,
                         arcade.color.BLACK, 40, 80, 'left')

    def initialize_grid(self):
        # Create a list of solid-color sprites to represent each grid location
        for row in range(self.x_size):
            for column in range(self.y_size):
                if self.map[row, column] == 255:
                    sprite = arcade.SpriteSolidColor(1, 1, arcade.color.WHITE)
                else:
                    sprite = arcade.SpriteSolidColor(1, 1, (self.map[row, column], 0, 0))

                sprite.center_x = column
                sprite.center_y = self.x_size - row
                self.grid_sprite_list.append(sprite)

    @staticmethod
    def _convert_to_binary_map(path):
        img = Image.open(path)
        img = img.convert("L")
        return np.array(img)
