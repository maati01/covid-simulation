import random
import threading
from logic.point import Point
from random import choices
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


class SimulateThread(threading.Thread):
    all_threads_finished_moving = False

    def __init__(self, points: dict[tuple[int, int], Point], all_cords: list[tuple[int, int]],
                 simulate_form_to: tuple[int, int]):
        super().__init__()
        self._points = points
        self._all_cords = all_cords
        self._reduced_cords = self._all_cords[simulate_form_to[0]: simulate_form_to[1]]
        self._finished_moving = False

    @property
    def finished_moving(self):
        return self._finished_moving

    def move_to_neighbours(self, point: Point, infected_to_neighbours: int):
        neighbours_cords = [(p.x, p.y) for p in point.neighbours]
        random.shuffle(neighbours_cords)
        for cords in neighbours_cords[:-1]:
            to_neighbour = round(random.random() * infected_to_neighbours)
            infected_to_neighbours -= to_neighbour
            self._points[cords].arrived_infected += to_neighbour
        self._points[neighbours_cords[-1]].arrived_infected += infected_to_neighbours

    def move_out_neighbours(self, infected_out_neighbours: int):
        moving_positions_out = choices(self._all_cords, k=infected_out_neighbours)
        counter = Counter(moving_positions_out)
        for moving_cord in counter.keys():
            self._points[moving_cord].arrived_infected += counter[moving_cord]

    def run(self):
        for cord in self._reduced_cords:
            point = self._points[cord]
            infected_to_neighbours, infected_out_neighbours = point.model.get_moving_infected_people()

            self.move_to_neighbours(point, infected_to_neighbours)
            self.move_out_neighbours(infected_out_neighbours)

        self._finished_moving = True
        while not self.all_threads_finished_moving:
            pass

        for cord in self._reduced_cords:
            self._points[cord].simulate()
