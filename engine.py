import arcade
import numpy as np
from GUI.gui import GUI
from logic.point import Point
from logic.SEIR import SEIR
import math

PATH_TO_BINARY_ARRAY = "data/binary_array.npy"
PATH_TO_POPULATION_ARRAY = "data/population_array.npy"


class Engine:
    def __init__(self):
        self.is_running = True
        self.points = self._create_matrix_of_points()
        self._set_points_by_distance_for_points()
        self.gui = GUI(PATH_TO_BINARY_ARRAY, self.points)

        # TODO initial chorzy
        # TODO run and check
        arcade.run()

    @staticmethod
    def _create_matrix_of_points():
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

    @staticmethod
    def _calculate_distance(point1, point2):
        return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

    def _set_points_by_distance_for_points(self):
        for point in self.points.values():
            point_distances = [
                (other, self._calculate_distance(point, other)) for other in self.points.values() if other != point
            ]
            point.points_sorted_by_distance = sorted(point_distances, key=lambda tup: tup[1])
