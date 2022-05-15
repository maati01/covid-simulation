import threading
from logic.point import Point
from random import choices
from collections import Counter


class SimulateThread(threading.Thread):
    all_threads_finished_moving = False

    def __init__(self, points: dict[tuple[int, int], Point], all_cords: list[tuple[int, int]],
                 simulate_form_to: tuple[int, int]):
        super().__init__()
        self._points = points
        self._all_cords = all_cords
        self._reduced_cords = self._all_cords[simulate_form_to[0] : simulate_form_to[1]]
        self._finished_moving = False

    @property
    def finished_moving(self):
        return self._finished_moving

    def run(self):
        for cord in self._reduced_cords:
            point = self._points[cord]
            infected_to_neighbours, infected_out_neighbours = point.model.get_moving_I_people()
            sum_ = infected_to_neighbours + infected_out_neighbours

            moving_positions = choices(self._all_cords, k=sum_)
            counter = Counter(moving_positions)
            for moving_cord in counter.keys():
                self._points[moving_cord].arrived_infected += counter[moving_cord]

        self._finished_moving = True
        while not self.all_threads_finished_moving:
            pass
        for cord in self._reduced_cords:
            self._points[cord].simulate()
