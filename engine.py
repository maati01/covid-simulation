import arcade
import numpy as np
from GUI.gui import GUI
from logic.point import Point
from logic.SEIR import SEIR
from helper.config import set_mode

class Engine:
    def __init__(self):
        scale, path_to_binary_array, path_to_population_array = set_mode()

        self.points = self._create_matrix_of_points(path_to_population_array)
        self.gui = GUI(path_to_binary_array, self.points, scale=scale)

        # TODO macierz pointow
        # TODO initial chorzy
        # TODO run and check
        arcade.run()

    def _create_matrix_of_points(self, path: str):
        populations = np.load(path)
        n, m = len(populations), len(populations[0])
        points = {}
        for i in range(n):
            for j in range(m):
                if populations[i, j] > 0:
                    point = Point(populations[i, j], x=i, y=j)
                    point.model = SEIR
                    points[(i, j)] = point

        return points
