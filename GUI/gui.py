import arcade
import numpy as np
from PIL import Image

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"


class GUI(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, path):
        """
        Set up the application.
        """
        #TODO zapisac mapke, bedzie sie szybciej uruchamiac

        self.map = self._convert_to_binary_map(path)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        super().__init__(self.y_size, self.x_size, SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        # Set the window's background color
        self.background_color = arcade.color.BLACK
        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()
        self.initialize_grid()

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()

    def initialize_grid(self):
        # Create a list of solid-color sprites to represent each grid location
        for row in range(self.x_size):
            for column in range(self.y_size):
                if self.map[row, column] == 255:
                    sprite = arcade.SpriteSolidColor(1, 1, arcade.color.WHITE)
                else:
                    sprite = arcade.SpriteSolidColor(1, 1, (self.map[row, column],0,0))

                sprite.center_x = column
                sprite.center_y = self.x_size - row
                self.grid_sprite_list.append(sprite)

    @staticmethod
    def _convert_to_binary_map(path):
        img = Image.open(path)
        img = img.convert("L")
        return np.array(img)
