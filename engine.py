from GUI.gui import GUI
from logic.point import Point
from logic.models import GenericModel
from helper.config import set_mode
import numpy as np
import arcade


class Engine:
    """Class to prepare and run simulation"""
    def __init__(self):
        scale, path_to_binary_array, path_to_population_array, path_to_color_abr, model = set_mode()

        self.points = self._create_matrix_of_points(path_to_population_array, model)
        self.gui = GUI(path_to_binary_array, path_to_color_abr, self.points, model(None), scale=scale)

        arcade.run()

    @staticmethod
    def _create_matrix_of_points(path: str, model: GenericModel):
        """Method creating 2D list of Points"""
        populations = np.load(path)

        points = {}
        for i, j in np.argwhere(populations > 0):
            point = Point(populations[i, j], x=i, y=j)
            point.model = model
            points[i, j] = point

        for i, j in points.keys():
            point = points[i, j]
            for cord in zip((-1, -1, -1, 0, 0, 1, 1, 1), (1, 0, -1, 1, -1, 1, 0, -1)):
                x, y = cord[0] + point.x, cord[1] + point.y
                if (x, y) in points:
                    point.neighbours.append(points[x, y])

        return points
