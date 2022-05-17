from logic.point import Point
from abc import ABC, abstractmethod
from random import choices, shuffle
from math import ceil, floor

# Italy params from link below
kappa = 0.012
gamma = 0.017
beta = 1 #0.22

# http://web.pdx.edu/~gjay/teaching/mth271_2020/html/09_SEIR_model.html
class GenericModel(ABC):
    def __init__(self, point: Point):
        self._point = point

    @abstractmethod
    def simulate(self):
        """Abstarct method to simulate point"""
        pass

# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7277829/#:~:text=The%20classical%20SEIR%20model%20can%20be%20described%20by%20a%20series%20of%20ordinary%20differential%20equations%3A
class SEIR(GenericModel):
    def simulate(self):
        """Func to simulate point with SEIR model"""
        n, i = [p + self._point.arrived_infected for p in (self._point.N, self._point.I)]
        s_div_n = self._point.S / n
        e, r = self._point.E, self._point.R

        beta_i_s_div_n, gamma_e, gamma_and_kappa_I = round(beta * self._point.I * s_div_n), round(gamma * e), round((gamma+kappa) * i)
        new_s, new_e, new_i, new_r = (
            self._point.S - beta_i_s_div_n,
            self._point.E + beta_i_s_div_n - gamma_e,
            self._point.I + gamma_e - gamma_and_kappa_I,
            self._point.R + gamma_and_kappa_I
        )

        if new_i < self._point.arrived_infected:
            diff = self._point.arrived_infected - new_i
            new_i += diff
            new_r -= diff

        self._point.S, self._point.E, self._point.I, self._point.R = new_s, new_e, new_i, new_r
        self._point.arrived_infected = 0

    def get_moving_I_people(self):
        """getting number of moving infected people"""
        people_to_move = round(self._point.N * self._point.move_probability)
        to_neighbours = round(people_to_move * self._point.neighbours_move_probability)

        moving_states = choices(
            ['S', 'E', 'I', 'R'],
            [val / self._point.N for val in [self._point.S, self._point.E, self._point.I, self._point.R]],
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
