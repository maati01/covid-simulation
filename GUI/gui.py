from logic.models import SEIR, SEIQR, SEIQRD, SEIQRD2V
from statistics.statistics import Statistics, StatisticsSEIR
from matplotlib.colors import ListedColormap
from logic.point import Point
from logic.threads import SimulateThread
import numpy as np
import arcade
import arcade.gui
import matplotlib

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Covid Simulation"
TEXT_PADDING = 40
FONT_SIZE = 25
DAY_FONT_SIZE = 40
TEXT_WIDTH = 80


# TODO uzyc center_window()
class GUI(arcade.Window):
    """Main application class."""

    def __init__(self, path_to_array: str, path_to_color_bar: str, points: dict[tuple[int, int], Point],
                 model: SEIR, threads_num=8, scale=1):
        """Set up the application."""
        statistics = {SEIR: StatisticsSEIR}
        self.map = np.load(path_to_array)
        self.x_size = len(self.map)
        self.y_size = len(self.map[0])
        self.scale = scale
        self.model = model
        self.color_bar_list = self._create_color_bar()

        # TODO chwilowo rozmiary mapki wejsciowej, trzeba przeskalowac
        super().__init__(self.y_size * scale + 1000, self.x_size * scale + 100, SCREEN_TITLE)

        # Creating a UI MANAGER to handle the UI
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Creating Button using UIFlatButton
        self.start_button = arcade.gui.UIFlatButton(text="Start", width=200)

        self.color_bar_img = arcade.load_texture(path_to_color_bar)

        # Assigning our on_buttonclick() function
        self.is_running = False
        self.start_button.on_click = self.on_button_click

        # Adding button in our uimanager
        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", child=self.start_button))

        self.points = points
        self.all_cords = list(points.keys())

        self.day = 0
        self.statistics = statistics[model.__class__](model)
        self.statistics.generate_plot(self.day)

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
        """Method to create color bar"""
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue", "yellow", "red"])
        distance_list = [i for i in range(0, 256)]

        # convert your distances to color coordinates
        color_list = cmap(distance_list)

        return color_list

    def update_text(self):
        """Method to update current statistics"""
        stats = self.statistics.current_stats_representations
        shift = self.scale + 1

        arcade.draw_text(stats['day'], TEXT_PADDING, self.x_size * self.scale + TEXT_PADDING,
                         arcade.color.BLACK, DAY_FONT_SIZE, TEXT_WIDTH, 'left')
        arcade.draw_text(stats['susceptible'], self.y_size * shift, self.x_size * self.scale + TEXT_PADDING,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(stats['exposed'], self.y_size * shift, self.x_size * self.scale,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(stats['infected'], self.y_size * shift, self.x_size * self.scale - TEXT_PADDING,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(stats['recovered'], self.y_size * shift, self.x_size * self.scale - TEXT_PADDING * 2,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)
        arcade.draw_text(stats['new_cases'], self.y_size * shift, self.x_size * self.scale - TEXT_PADDING * 3,
                         arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)

        if isinstance(self.model, SEIQR):
            arcade.draw_text(stats['quarantined'], self.y_size * (shift + 2.5), self.x_size * self.scale + TEXT_PADDING,
                             arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)

        if isinstance(self.model, SEIQRD):  # SEIQRD2 also works
            arcade.draw_text(stats['deaths'], self.y_size * (shift + 2.5), self.x_size * self.scale,
                             arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)

        if isinstance(self.model, SEIQRD2V):
            arcade.draw_text(stats['vaccinated'], self.y_size * (shift + 2.5), self.x_size * self.scale - TEXT_PADDING,
                             arcade.color.BLACK, FONT_SIZE, TEXT_WIDTH)

    def simulate(self, delta_time: float):
        """Method to simulate one day"""
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
        self.statistics.update_day()
        self.statistics.update_data_file()

        self.day += 1
        self.statistics.generate_plot(self.day)

    def on_draw(self) -> None:
        """Render the screen."""
        arcade.start_render()

        # We should always start by clearing the window pixels
        self.clear()

        self.grid_sprite_list.draw()

        self.statistics.reset_statistics()

        for point in self.points.values():
            if point.all_infected() > 0:
                idx = int((point.all_infected() / point.N) * 255)
                # if point.N < 20:
                #     print(point.all_infected, point.N)
                new_color = tuple([val * 255 for val in self.color_bar_list[idx]])
                self.grid_sprites[point.x][point.y].color = new_color
            elif point.all_infected() == 0:
                self.grid_sprites[point.x][point.y].color = (0, self.map[point.x, point.y], 0)
            self.statistics.update_statistics(point)

        # Batch draw all the sprites

        self.uimanager.draw()
        self.update_text()

        arcade.draw_texture_rectangle(self.x_size * self.scale + 120, self.y_size * self.scale - 350,
                                      self.color_bar_img.width * 0.8,
                                      self.color_bar_img.height * 0.8, self.color_bar_img, 0)

        plot = arcade.load_texture(f"data/plot/plot{self.day}.png")
        arcade.draw_texture_rectangle(self.x_size * self.scale + 600, self.y_size * self.scale - 400,
                                      plot.width * 0.8,
                                      plot.height * 0.8, plot, 0, 255)

    def initialize_grid(self) -> None:
        """Method creating a list of solid-color sprites to represent each grid location"""
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
        """Method called when the user presses a mouse button."""
        temp = x
        x = self.x_size - int(y // self.scale)
        y = int(temp // self.scale)

        try:
            if self.points[x, y].S > 0:
                self.points[x, y].I[0] += 1
                self.points[x, y].S -= 1
        except KeyError:
            pass

    def on_button_click(self, event):
        """This method will be called everytime the user presses the button"""

        if self.is_running:
            self.start_button.text = "Start"
            self.is_running = False
        else:
            self.start_button.text = "Stop"
            self.is_running = True
