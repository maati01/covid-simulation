from logic.point import Point
from abc import ABC, abstractmethod
from random import choices, shuffle
from math import ceil, floor

# Italy params from link below
kappa = 0.012
gamma = 0.21
beta = 0.56  # 0.22


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

        beta_i_s_div_n, gamma_e, gamma_and_kappa_I = round(beta * i * s_div_n), round(gamma * e), round(
            (gamma + kappa) * i)
        new_s, new_e, new_i, new_r = (
            self._point.S - beta_i_s_div_n,
            e + beta_i_s_div_n - gamma_e,
            i + gamma_e - gamma_and_kappa_I,
            r + gamma_and_kappa_I
        )

        new_i -= self._point.arrived_infected
        if new_i < 0:
            new_r, new_i = new_r + new_i, 0

        if new_r < 0:
            print("ARRIVED INF: ", self._point.arrived_infected)
            print(f"s {self._point.S}, i {self._point.I}, r {self._point.R}, e {self._point.E}")
            print(f"new s {new_s}, new i {new_i}, new_r {new_r}, new e {new_e}")
            print(f"beta {beta_i_s_div_n}, gamma {gamma_e}, gamma_kappa {gamma_and_kappa_I}")

        self._point.S, self._point.E, self._point.I, self._point.R = new_s, new_e, new_i, new_r
        self._point.arrived_infected = 0

    def get_moving_I_people(self):
        """getting number of moving infected people"""
        people_to_move = round(self._point.N * self._point.move_probability)
        to_neighbours = round(people_to_move * self._point.neighbours_move_probability)

        weights = [val / self._point.N for val in [self._point.S, self._point.E, self._point.I, self._point.R]]
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

        if infected_out_neighbours + infected_to_neighbours > self._point.I:
            difference = infected_out_neighbours + infected_to_neighbours - self._point.I
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
