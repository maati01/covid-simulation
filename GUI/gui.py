import arcade
import numpy as np
from typing import List
from logic.point import Point
from random import randint
import dill
import weakref
from copy import deepcopy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 50


# TODO uzyc center_window()
class GUI(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, path: str, points: dict[tuple[int, int], Point]):
        """
        Set up the application.
        """

        self.map = np.load(path)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        super().__init__(self.y_size, self.x_size + 100,
                         SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        self.points = points
        self.day = 0
        self.text = f"Day: {self.day}"
        # Set the window's background color
        self.background_color = arcade.color.WHITE
        # Create a spritelist for batch drawing all the grid sprites

        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []

        self.initialize_grid()
        #arcade.schedule(self.update_day, 5)
        arcade.schedule(self.simulate, 5)

    def update_day(self, delta_time: float) -> None:
        """
        Update days.
        """
        self.day += 1
        self.text = f"Day: {self.day}"

    def simulate(self, delta_time: float):
        for point in self.points.values():
            infected_to_neighbours, infected_out_neighbours = point.model.get_moving_I_people()
            sum_ = infected_to_neighbours + infected_out_neighbours
            x, y = randint(100, 600), randint(100, 600)
            while not self.points.__contains__((x, y)): #TODO nie wrzucac wszystkich do jednego pointa
                x, y = randint(100, 600), randint(100, 600)
            self.points[(x, y)].arrived_infected = sum_

        for point in self.points.values():
            point.simulate()

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

        for point in self.points.values():
            if point.I > 0:
                self.grid_sprites[point.x][point.y].color = arcade.color.GOLD

    def initialize_grid(self, load=False) -> None:
        # Create a list of solid-color sprites to represent each grid location
        if load:
            self.grid_sprites = dill.loads(open("data\\grid_sprites", "rb"))
            self.grid_sprite_list = dill.loads(open("data\\grid_sprite_list", "rb"))
        else:
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

            dill.dumps(deepcopy(self.grid_sprites), open("data\\grid_sprites", "wb"))
            dill.dumps(deepcopy(self.grid_sprite_list), open("data\\grid_sprite_list", "wb"))

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        color = arcade.color.GREEN

        for i in range(10):
            for j in range(10):
                self.grid_sprites[self.x_size - int(y) + i][int(x) + j].color = color
                self.points[(self.x_size - int(y) + i, int(x) + j)].I = self.points[
                    (self.x_size - int(y) + i, int(x) + j)].N
                self.points[(self.x_size - int(y) + i, int(x) + j)].S = 0
