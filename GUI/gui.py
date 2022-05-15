import arcade
import arcade.gui
import numpy as np
from logic.point import Point
from logic.threads import SimulateThread

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 50


# TODO uzyc center_window()


class GUI(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, path: str, points: dict[tuple[int, int], Point], threads_num=8, scale=1):
        """
        Set up the application.
        """
        self.map = np.load(path)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        self.scale = scale

        super().__init__(self.y_size * scale, self.x_size * scale + 100,
                         SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        # Creating a UI MANAGER to handle the UI
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Creating Button using UIFlatButton
        self.start_button = arcade.gui.UIFlatButton(text="Start", width=200)

        # Assigning our on_buttonclick() function
        self.is_running = False
        self.start_button.on_click = self.on_button_click

        # Adding button in our uimanager
        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.start_button))

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
        arcade.schedule(self.simulate, 1)

    def update_day(self, delta_time: float) -> None:
        """
        Update days.
        """
        self.day += 1
        self.text = f"Day: {self.day}"

    def simulate(self, delta_time: float):
        if not self.is_running:
            return

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
        arcade.start_render()

        # We should always start by clearing the window pixels
        # self.clear()

        for point in self.points.values():
            prev_color = self.grid_sprites[point.x][point.y].color
            g = round((point.I / point.N) * 255)
            new_color = (self.grid_sprites[point.x][point.y].color[0], g, 0)
            if new_color != prev_color:
                self.grid_sprites[point.x][point.y].color = arcade.color.GOLD

        # Batch draw all the sprites
        self.grid_sprite_list.draw()

        self.uimanager.draw()

        arcade.draw_text(self.text, TEXT_PADDING, self.x_size * self.scale + TEXT_PADDING,
                         arcade.color.BLACK, 40, 80, 'left')

    def initialize_grid(self) -> None:
        # Create a list of solid-color sprites to represent each grid location

        for row in range(self.x_size):
            self.grid_sprites.append([])
            for column in range(self.y_size):
                sprite = arcade.SpriteSolidColor(self.scale, self.scale, arcade.color.WHITE)
                if self.map[row, column] != 255:
                    sprite.color = (self.map[row, column], 0, 0)

                sprite.center_x = column * self.scale
                sprite.center_y = (self.x_size - row) * self.scale
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        color = arcade.color.GREEN

        temp = x
        x = self.x_size - int(y // self.scale)
        y = int(temp // self.scale)

        self.grid_sprites[x][y].color = color
        self.points[x, y].I = self.points[x, y].N
        self.points[x, y].S = 0

    def on_button_click(self, event):
        """
        This function will be called everytime the user presses the button
        """

        if self.is_running:
            self.start_button.text = "Start"
            self.is_running = False
        else:
            self.start_button.text = "Stop"
            self.is_running = True
