from logic.point import Point
from abc import ABC, abstractmethod
from random import choices, shuffle
from math import ceil, floor

beta = 0.45
sigma = 0.1
gamma = 0.1

# http://web.pdx.edu/~gjay/teaching/mth271_2020/html/09_SEIR_model.html
class GenericModel(ABC):
    def __init__(self, point: Point):
        self._point = point

    @abstractmethod
    def simulate(self):
        """Abstarct method to simulate point"""
        pass


class SEIR(GenericModel):
    def simulate(self):
        """Func to simulate point with SEIR model"""
        n = self._point.N + self._point.arrived_infected
        s, e, i, r = [val / n for val in
                      (self._point.S, self._point.E, self._point.I + self._point.arrived_infected, self._point.R)]

        new_s = self._point.S - beta * i * s
        new_e = self._point.E + (beta * i * s - sigma * e)
        new_i = self._point.I + sigma * e - gamma * i
        new_r = self._point.R + gamma * i

        if new_i < self._point.arrived_infected:
            diff = self._point.arrived_infected - new_i
            new_i += diff
            new_r -= diff

        self._point.S, self._point.E, self._point.I, self._point.R = new_s, new_e, new_i, new_r

    def get_moving_I_people(self):
        """getting number of moving infected people"""
        people_to_move = round(self._point.N * self._point.move_probability)
        to_neighbours = round(people_to_move * self._point.neighbours_move_probability)

        #TODO wyjebac tego maxa XDD
        moving_states = choices(
            ['S', 'E', 'I', 'R'],
            [val / max(self._point.N, 1) for val in [self._point.S, self._point.E, self._point.I, self._point.R]],
            k=people_to_move
        )

        shuffle(moving_states)
        moving_states_to_neighbours = moving_states[:to_neighbours]
        moving_states_out_neighbours = moving_states[to_neighbours:]

        infected_to_neighbours = moving_states_to_neighbours.count('I')
        infected_out_neighbours = moving_states_out_neighbours.count('I')

        if infected_out_neighbours + infected_to_neighbours > self._point.I:
            difference = infected_out_neighbours + infected_to_neighbours - self._point.I
            half_of_difference = difference / 2

            infected_out_neighbours -= ceil(half_of_difference)
            infected_to_neighbours -= floor(half_of_difference)

        return infected_to_neighbours, infected_out_neighbours
