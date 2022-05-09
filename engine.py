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
        self.gui = GUI(PATH_TO_BINARY_ARRAY)
        self.points_matrix = self._create_matrix_of_points()

        #TODO macierz pointow
        #TODO initial chorzy
        #TODO run and check
        arcade.run()

    def _create_matrix_of_points(self):
        populations = np.load(PATH_TO_POPULATION_ARRAY)
        n, m = len(populations), len(populations[0])

        matrix = [[None for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if populations[i, j] > 0:
                    point = Point(populations[i, j])
                    point.model = SEIR
                    matrix[i][j] = point

        return matrix


