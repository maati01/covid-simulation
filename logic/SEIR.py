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

        beta_i_s_div_n, gamma_e, gamma_and_kappa_I = \
            round(beta * i * s_div_n), round(gamma * e_able_to_infected), round((gamma + kappa) * i_able_to_recover)

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

    def get_moving_I_people(self):
        """getting number of moving infected people"""
        people_to_move = round(self._point.N * self._point.move_probability)
        to_neighbours = round(people_to_move * self._point.neighbours_move_probability)

        weights = [val / self._point.N for val in
                   [self._point.S, self._point.all_exposed, self._point.all_infected, self._point.R]]
        states = ['S', 'E', 'I', 'R']

        moving_states = choices(
            [states[i] for i in range(len(states)) if weights[i] > 0],
            [weight for weight in weights if weight > 0],
            k=people_to_move
        )

        shuffle(moving_states)
        moving_states_to_neighbours = moving_states[:to_neighbours]
        moving_states_out_neighbours = moving_states[to_neighbours:]

        infected_to_neighbours = moving_states_to_neighbours.count('I')
        infected_out_neighbours = moving_states_out_neighbours.count('I')

        if infected_out_neighbours + infected_to_neighbours > self._point.all_infected:
            difference = infected_out_neighbours + infected_to_neighbours - self._point.all_infected
            half_of_difference = difference / 2

            infected_out_neighbours -= ceil(half_of_difference)
            infected_to_neighbours -= floor(half_of_difference)

            if infected_out_neighbours <= 0:
                infected_to_neighbours += infected_out_neighbours
                infected_out_neighbours = 0
                if infected_to_neighbours > 0:
                    out_of_to_neighbours = round((1 - self._point.neighbours_move_probability) * infected_to_neighbours)
                    infected_to_neighbours -= out_of_to_neighbours
                    infected_out_neighbours += out_of_to_neighbours
                else:
                    infected_to_neighbours = 0
            elif infected_to_neighbours < 0:
                infected_to_neighbours, infected_out_neighbours = infected_out_neighbours, 0

        return infected_to_neighbours, infected_out_neighbours
