import arcade
import numpy as np
from GUI.gui import GUI
from logic.point import Point
from logic.SEIR import SEIR

PATH_TO_BINARY_ARRAY = "data/binary_array.npy"
PATH_TO_POPULATION_ARRAY = "data/population_array.npy"


class Engine:
    def __init__(self):
        self.is_running = True

        self.points = self._create_matrix_of_points()
        self.gui = GUI(PATH_TO_BINARY_ARRAY, self.points)

        # TODO macierz pointow
        # TODO initial chorzy
        # TODO run and check
        arcade.run()

    def _create_matrix_of_points(self):
        populations = np.load(PATH_TO_POPULATION_ARRAY)
        n, m = len(populations), len(populations[0])
        points = {}
        for i in range(n):
            for j in range(m):
                if populations[i, j] > 0:
                    point = Point(populations[i, j], x=i, y=j)
                    point.model = SEIR
                    points[(i, j)] = point

        return points
