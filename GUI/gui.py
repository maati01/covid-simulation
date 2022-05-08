import arcade
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 50


# TODO uzyc center_window()
class GUI(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, path: str):
        """
        Set up the application.
        """

        self.map = np.load(path)
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
        self.grid_sprites = []

        self.initialize_grid()
        arcade.schedule(self.update_day, 1)

    def update_day(self, delta_time: float) -> None:
        """
        Update days.
        """
        self.day += 1
        self.text = f"Day: {self.day}"

    def on_draw(self) -> None:
        """
        Render the screen.
        """
        # arcade.start_render()

        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()
        arcade.draw_text(self.text, TEXT_PADDING, self.x_size + TEXT_PADDING,
                         arcade.color.BLACK, 40, 80, 'left')

    def initialize_grid(self) -> None:
        # Create a list of solid-color sprites to represent each grid location

        for row in range(self.x_size):
            self.grid_sprites.append([])
            for column in range(self.y_size):
                sprite = arcade.SpriteSolidColor(1, 1, arcade.color.WHITE)
                if self.map[row, column] != 255:
                    sprite.color = (self.map[row, column], 0, 0)

                sprite.center_x = column
                sprite.center_y = self.x_size - row
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.grid_sprites[self.x_size - int(y)][int(x)].color == arcade.color.GREEN:
            color = arcade.color.YELLOW
        else:
            color = arcade.color.GREEN
        for i in range(100):
            for j in range(100):
                self.grid_sprites[self.x_size - int(y) + i][int(x) + j].color = color
