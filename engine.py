import arcade
import numpy as np
from GUI.gui import GUI
from logic.point import Point
from logic.SEIR import SEIR
from helper.config import set_mode
from logic.threads import GraphRunner


class Engine:
    def __init__(self):
        scale, path_to_binary_array, path_to_population_array, path_to_color_abr = set_mode()

        self.points = self._create_matrix_of_points(path_to_population_array)
        self.gui = GUI(path_to_binary_array, path_to_color_abr, self.points, scale=scale)

        plot_thread = GraphRunner()
        plot_thread.daemon = True
        plot_thread.start()
        arcade.run()
        GraphRunner.stop = True

    @staticmethod
    def _create_matrix_of_points(path: str):
        populations = np.load(path)
        # n, m = len(populations), len(populations[0])

        points = {}
        for i, j in np.argwhere(populations > 0):
            point = Point(populations[i, j], x=i, y=j)
            point.model = SEIR
            points[i, j] = point

        for i, j in points.keys():
            point = points[i, j]
            for cord in zip((-1, -1, -1, 0, 0, 1, 1, 1), (1, 0, -1, 1, -1, 1, 0, -1)):
                x, y = cord[0] + point.x, cord[1] + point.y
                if (x, y) in points:
                    point.neighbours.append(points[x, y])

        return points
