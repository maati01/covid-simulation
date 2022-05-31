import random

from logic.point import Point
from abc import ABC, abstractmethod
from random import choices, shuffle
from math import ceil, floor

# Italy params from link below
kappa = 0.012
gamma = 0.4
beta = 0.69


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
        i_able_to_recover, e_able_to_infected = self._point.I[-1], self._point.E[-1]
        n, i = [p + self._point.arrived_infected for p in (self._point.N, sum(self._point.I))]
        s_div_n = self._point.S / n

        round_func = floor if random.random() > 0.5 else ceil
        beta_i_s_div_n, gamma_e, gamma_and_kappa_I = \
            round_func(beta * i * s_div_n), round_func(gamma * e_able_to_infected), round_func((gamma + kappa) * i_able_to_recover)

        delta_s, new_e, delta_e, new_i, delta_i, delta_r = (
            -beta_i_s_div_n,
            beta_i_s_div_n,
            -gamma_e,
            gamma_e,
            -gamma_and_kappa_I,
            gamma_and_kappa_I
        )

        self._point.S += delta_s
        self._point.E[-1] += delta_e
        self._point.I[-1] += delta_i
        self._point.R += delta_r
        self._point.arrived_infected = 0
        self._point.move_lists_stats(new_e, new_i)

    def get_moving_infected_people(self):
        """getting number of moving infected people"""

        infected_to_move = round(self._point.all_infected * random.uniform(0.01, 0.3))

        infected_to_neighbours = round(infected_to_move * self._point.neighbours_move_probability)
        infected_out_neighbours = infected_to_move - infected_to_neighbours

        # liczenie czy faktycznie ida out_neighbours
        rand = random.random()
        if rand > 0.5:
            infected_out_neighbours = 0
        elif rand > 0.1:
            infected_out_neighbours = round(infected_out_neighbours * random.uniform(0, 0.7))

        return infected_to_neighbours, infected_out_neighbours
