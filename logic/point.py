from random import choices, shuffle


class Point:
    def __init__(self, init_N: int, province: str):  # TODO province should be enum I think
        self._N = init_N
        self._province = province
        self._S = init_N
        self._E = 0
        self._I = 0
        self._R = 0
        # self.neighbours = list()
        # self.move_probability = 0.5
        # self.neighbours_move_probability = 0.7
        # self.S_moved = 0
        # self.E_moved = 0
        # self.I_moved = 0
        # self.R_moved = 0

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

    # def _get_list_of_moving_people(self, n: int):
    #     """create list of people (represented by states) which will move to different point"""
    #     moving_states = list()
    #     for i in range(n):
    #         new_state = choices(['S', 'E', 'I', 'R'], [val / self.N for val in [self.S, self.E, self.I, self.R]])[0]
    #
    #         self.N -= 1
    #         if new_state == 'S':
    #             self.S -= 1
    #             self.S_moved += 1
    #         elif new_state == 'E':
    #             self.E -= 1
    #             self.E_moved += 1
    #         elif new_state == 'I':
    #             self.I -= 1
    #             self.I_moved += 1
    #         else:
    #             self.R -= 1
    #             self.R_moved += 1
    #
    #         moving_states.append(new_state)
    #
    #     shuffle(moving_states)
    #     return moving_states
    #
    # def get_moving_people(self):
    #     """getting which people are moving"""
    #     people_to_move = round(self.N * self.move_probability)
    #     to_neighbours = round(people_to_move * self.neighbours_move_probability)
    #     out_neighbours = people_to_move - to_neighbours
    #
    #     moving = dict()
    #     moving['to_neighbours'] = dict()
    #     moving['out_neighbours'] = dict()
    #
    #     moving_states = self._get_list_of_moving_people(people_to_move)
