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

    def run(self):
        for cord in self._reduced_cords:
            point = self._points[cord]
            infected_to_neighbours, infected_out_neighbours = point.model.get_moving_I_people()

            moving_positions_to = choices([(p.x, p.y) for p in point.neighbours], k=infected_to_neighbours)
            moving_positions_out = choices(self._all_cords, k=infected_out_neighbours) #TODO without neighbours and self
            moving_positions = moving_positions_out + moving_positions_to
            counter = Counter(moving_positions)
            for moving_cord in counter.keys():
                self._points[moving_cord].arrived_infected += counter[moving_cord]

        self._finished_moving = True
        while not self.all_threads_finished_moving:
            pass

        for cord in self._reduced_cords:
            self._points[cord].simulate()


class GraphRunner(threading.Thread):
    stop = False

    def kill(self):
        self._stop.set()

    def animate(self, i):
        print(self.stop)
        if self.stop:
            self.ani.event_source.stop()

        data = pd.read_csv('statistics/data.csv')
        day = data['Day']
        susceptible = data['Susceptible']
        exposed = data['Exposed']
        infective = data['Infective']
        recovered = data['Recovered']

        plt.cla()

        # plt.plot(day, susceptible, label='Susceptible')
        plt.plot(day, exposed, label='Exposed')
        plt.plot(day, infective, label='Infective')
        plt.plot(day, recovered, label='Recovered')

        plt.legend(loc='upper left')
        plt.tight_layout()

    def run(self):
        plt.style.use('fivethirtyeight')
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.tight_layout()
        plt.show()
