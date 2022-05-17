import arcade
import arcade.gui
import matplotlib
import numpy as np
from matplotlib.colors import ListedColormap

from logic.point import Point
from logic.threads import SimulateThread

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 50
FONT_SIZE = 40
TEXT_WIDTH = 80
PATH_TO_COLOR_BAR = "data/colorbar.jpg"


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

        self.color_bar_list = self._create_color_bar()

        super().__init__(self.y_size * scale + 600, self.x_size * scale + 100,
                         SCREEN_TITLE)  # chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac

        # Creating a UI MANAGER to handle the UI
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Creating Button using UIFlatButton
        self.start_button = arcade.gui.UIFlatButton(text="Start", width=200)

        self.color_bar_img = arcade.load_texture(PATH_TO_COLOR_BAR)

        # Assigning our on_buttonclick() function
        self.is_running = False
        self.start_button.on_click = self.on_button_click

        # Adding button in our uimanager
        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.start_button))

        self.points = points
        self.all_cords = list(points.keys())
        self.day = 0
        self.text = f"Day: {self.day}"

        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infective_cnt = 0
        self.recovered_cnt = 0

        self.susceptible = f"susceptible: {self.susceptible_cnt}"
        self.exposed = f"exposed: {self.exposed_cnt}"
        self.infective = f"infective: {self.infective_cnt}"
        self.recovered = f"recovered: {self.recovered_cnt}"

        # Set the window's background color
        self.background_color = arcade.color.WHITE
        # Create a spritelist for batch drawing all the grid sprites

        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []

        self._threads_num = threads_num
        self.initialize_grid()
        arcade.schedule(self.simulate, 1)

    @staticmethod
    def _create_color_bar():
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue", "yellow", "red"])
        distance_list = [i for i in range(0, 256)]

        # convert your distances to color coordinates
        color_list = cmap(distance_list)

        return color_list

    def update_day(self):
        self.day += 1
        self.text = f"Day: {self.day}"

    def update_info(self):
        self.susceptible = f"susceptible: {self.susceptible_cnt}"
        self.exposed = f"exposed: {self.exposed_cnt}"
        self.infective = f"infective: {self.infective_cnt}"
        self.recovered = f"recovered: {self.recovered_cnt}"

    def reset_counters(self):
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infective_cnt = 0
        self.recovered_cnt = 0

    # TODO z jakiegos powodu musze tutaj mnozyc, bo przy zapisywaniu arraya spowalnia program
    def update_counters(self, point: Point):
        self.susceptible_cnt += point.S * (self.scale ** 2)
        self.exposed_cnt += point.E * (self.scale ** 2)
        self.infective_cnt += point.I * (self.scale ** 2)
        self.recovered_cnt += point.R * (self.scale ** 2)

    def update_text(self):
        arcade.draw_text(self.text, TEXT_PADDING, self.x_size * self.scale + TEXT_PADDING,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH, 'left')

        arcade.draw_text(self.susceptible, self.y_size * self.scale, self.x_size * self.scale + TEXT_PADDING,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(self.exposed, self.y_size * self.scale, self.x_size * self.scale,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(self.infective, self.y_size * self.scale, self.x_size * self.scale - TEXT_PADDING,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(self.recovered, self.y_size * self.scale, self.x_size * self.scale - TEXT_PADDING * 2,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)

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
        self.update_day()
        self.update_info()

    def on_draw(self) -> None:
        """
        Render the screen.
        """
        arcade.start_render()

        # We should always start by clearing the window pixels
        self.clear()

        self.grid_sprite_list.draw()

        self.reset_counters()

        for point in self.points.values():
            if point.I > 0:
                idx = int((point.I / point.N) * 255)
                new_color = tuple([val * 255 for val in self.color_bar_list[idx]])
                self.grid_sprites[point.x][point.y].color = new_color
            self.update_counters(point)

        # Batch draw all the sprites

        self.uimanager.draw()
        self.update_text()

        arcade.draw_texture_rectangle(self.x_size * self.scale + 120, self.y_size * self.scale - 400,
                                      self.color_bar_img.width * 0.8,
                                      self.color_bar_img.height * 0.8, self.color_bar_img, 0)

    def initialize_grid(self) -> None:
        # Create a list of solid-color sprites to represent each grid location

        for row in range(self.x_size):
            self.grid_sprites.append([])
            for column in range(self.y_size):
                sprite = arcade.SpriteSolidColor(self.scale, self.scale, arcade.color.WHITE)
                if self.map[row, column] != 255:
                    sprite.color = (0, self.map[row, column], 0)
                sprite.center_x = column * self.scale
                sprite.center_y = (self.x_size - row) * self.scale
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        temp = x
        x = self.x_size - int(y // self.scale)
        y = int(temp // self.scale)

        self.points[x, y].I = self.points[(x, y)].N
        self.points[x, y].S = 0

        self.grid_sprites[x][y].color = arcade.color.RED

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
