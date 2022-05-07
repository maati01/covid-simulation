from random import choices, shuffle
from math import ceil, floor

class Point:
    def __init__(self, init_N: int, province: str):  # TODO province should be enum I think
        self._N = init_N
        self._province = province
        self._S = init_N
        self._E = 0
        self._I = 0
        self._R = 0
        self.neighbours = list()
        self.move_probability = 0.5
        self.neighbours_move_probability = 0.7
        self.arrived_infected = 0

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, value):
        self._N = value

    @property
    def S(self):
        return self._S

    @S.setter
    def S(self, value):
        self._S = value

    @property
    def E(self):
        return self._E

    @E.setter
    def E(self, value):
        self._E = value

    @property
    def I(self):
        return self._I

    @I.setter
    def I(self, value):
        self._I = value

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        self._R = value

    def simulate(self):
        """Simulate next day"""
        pass

    def get_moving_I_people(self):
        """getting number of moving infected people"""
        people_to_move = round(self.N * self.move_probability)
        to_neighbours = round(people_to_move * self.neighbours_move_probability)

        moving_states = choices(['S', 'E', 'I', 'R'], [val / self.N for val in [self.S, self.E, self.I, self.R]],
                                k=people_to_move)

        shuffle(moving_states)
        moving_states_to_neighbours = moving_states[:to_neighbours]
        moving_states_out_neighbours = moving_states[to_neighbours:]

        infected_to_neighbours = moving_states_to_neighbours.count('I')
        infected_out_neighbours = moving_states_out_neighbours.count('I')

        if infected_out_neighbours + infected_to_neighbours > self.I:
            difference = infected_out_neighbours + infected_to_neighbours - self.I
            half_of_difference = difference / 2

            infected_out_neighbours -= ceil(half_of_difference)
            infected_to_neighbours -= floor(half_of_difference)

        return infected_to_neighbours, infected_out_neighbours
