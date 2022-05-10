import arcade
import numpy as np
from typing import List
from logic.point import Point
from random import randint
from logic.threads import SimulateThread
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

    def __init__(self, path: str, points: dict[tuple[int, int], Point], threads_num=8):
        """
        Set up the application.
        """
        self.map = np.load(path)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        super().__init__(self.y_size, self.x_size + 100,
                         SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        self.points = points
        self.all_cords = list(points.keys())

        self.day = 0
        self.text = f"Day: {self.day}"
        # Set the window's background color
        self.background_color = arcade.color.WHITE
        # Create a spritelist for batch drawing all the grid sprites

        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []

        self._threads_num = threads_num
        self.initialize_grid()
        # arcade.schedule(self.update_day, 5)
        arcade.schedule(self.simulate, 5)

    def update_day(self, delta_time: float) -> None:
        """
        Update days.
        """
        self.day += 1
        self.text = f"Day: {self.day}"

    def simulate(self, delta_time: float):
        n = len(self.all_cords)
        threads_point_len = round(n / self._threads_num)
        from_to = [(0 + i * threads_point_len, threads_point_len + i * threads_point_len) for i in
                   range(self._threads_num - 1)]
        from_to.append((0 + (self._threads_num - 1) * threads_point_len, n))
        threads = [SimulateThread(self.points, self.all_cords, from_to[i]) for i in range(self._threads_num)]

        for thread in threads:
            thread.start()

        for thread in threads:
            while not thread.finished_moving:
                pass

        SimulateThread.all_threads_finished_moving = True

        for thread in threads:
            thread.join()

        SimulateThread.all_threads_finished_moving = False
        self.day += 1
        self.text = f"Day: {self.day}"

    def on_draw(self) -> None:
        """
        Render the screen.
        """
        # arcade.start_render()

        # We should always start by clearing the window pixels
        self.clear()

        for point in self.points.values():
            prev_color = self.grid_sprites[point.x][point.y].color
            g = round((point.I / point.N) * 255)
            new_color = (self.grid_sprites[point.x][point.y].color[0], g, 0)
            if new_color != prev_color:
                self.grid_sprites[point.x][point.y].color = arcade.color.GOLD

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

        color = arcade.color.GREEN

        for i in range(10):
            for j in range(10):
                self.grid_sprites[self.x_size - int(y) + i][int(x) + j].color = color
                self.points[(self.x_size - int(y) + i, int(x) + j)].I = \
                    self.points[(self.x_size - int(y) + i, int(x) + j)].N
                self.points[(self.x_size - int(y) + i, int(x) + j)].S = 0
