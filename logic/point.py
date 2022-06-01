class Point:
    def __init__(self, init_N: int, x: int, y: int, province: str = None, e_range: int = 2, i_range: int = 10,
                 q_range: int = 10):
        """
        :param init_N: number of people
        :param x: x coord
        :param y: y cord
        :param province: voivodeship (ex. Wielkopolska)
        :param e_range: num of days when people cannot change state and must be exposed
        :param i_range: num of days when people cannot change state and must be infected
        """
        # TODO province should be enum I think
        self.x = x
        self.y = y
        self._N = init_N
        self._province = province
        self._model = None
        self._S = init_N
        self._E = [0 for _ in range(e_range)]
        self._I = [0 for _ in range(i_range)]
        self._Q = [0 for _ in range(q_range)]
        self._E2 = [0 for _ in range(e_range)]
        self._I2 = [0 for _ in range(i_range)]
        self._Q2 = [0 for _ in range(q_range)]
        self._R = 0
        self._R2 = 0
        self._D = 0
        self._neighbours = list()
        self.move_probability = 0.8
        self.neighbours_move_probability = 0.95
        self.arrived_infected = 0

    def move_lists_stats(self, new_e: int, new_i: int, new_q: int = None, new_e2: int = None,
                         new_i2: int = None, new_q2: int = None):
        """Method to move people in lists. Just to get they able to change state in the future"""
        self.move_list_stats(self._E, new_e)
        self.move_list_stats(self._I, new_i)

        if new_q is not None:
            self.move_list_stats(self._Q, new_q)

        if new_e2 is not None:
            self.move_list_stats(self._E2, new_e2)

        if new_i2 is not None:
            self.move_list_stats(self._I2, new_i2)

        if new_q2 is not None:
            self.move_list_stats(self._Q2, new_q2)

    @staticmethod
    def move_list_stats(list_to_update: list[int], new_in_state: int):
        """
        Method to move people in one list
        :param list_to_update: either self._E or self._I
        :param new_in_state: people who just changed state
        """
        list_to_update[-1] += list_to_update[-2]
        for i in range(len(list_to_update) - 3, -1, -1):
            list_to_update[i + 1] = list_to_update[i]

        list_to_update[0] = new_in_state

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
    def E2(self):
        return self._E2

    @E2.setter
    def E2(self, value):
        self._E2 = value

    @property
    def all_exposed(self):
        return sum(self._E) + sum(self._E2)

    @property
    def I(self):
        return self._I

    @property
    def I2(self):
        return self._I2

    @property
    def all_infected(self):
        return sum(self._I) + sum(self._I2)

    @property
    def all_quarantined(self):
        return sum(self._Q) + sum(self._Q2)

    @property
    def Q(self):
        return self._Q

    @property
    def Q2(self):
        return self._Q2

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        self._R = value

    @property
    def R2(self):
        return self._R2

    @R2.setter
    def R2(self, value):
        self._R2 = value

    @property
    def all_recovered(self):
        return self._R + self._R2

    @property
    def D(self):
        return self._D

    @D.setter
    def D(self, value):
        self._D = value

    @property
    def model(self):
        return self._model

    @property
    def neighbours(self):
        return self._neighbours

    @neighbours.setter
    def neighbours(self, value):
        self._neighbours = value

    @model.setter
    def model(self, model_class):
        self._model = model_class(self)

    def simulate(self):
        """Simulate next day"""
        self._model.simulate()

    @I.setter
    def I(self, value):
        self._I = value

    @Q.setter
    def Q(self, value):
        self._Q = value

    @Q2.setter
    def Q2(self, value):
        self._Q2 = value

    @I2.setter
    def I2(self, value):
        self._I2 = value
