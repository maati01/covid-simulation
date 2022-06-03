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
        :param q_range: num of days when people cannot change state and must be on quarantine
        """
        # TODO province should be enum I think
        self.x = x
        self.y = y
        self._province = province
        self._N = init_N
        self._model = None
        self._S = init_N
        self._E = [0 for _ in range(e_range)]
        self._I = [0 for _ in range(i_range)]
        self._Q = [0 for _ in range(q_range)]
        self._R = 0
        self._D = 0
        self._E2 = [0 for _ in range(e_range)]
        self._I2 = [0 for _ in range(i_range)]
        self._Q2 = [0 for _ in range(q_range)]
        self._R2 = 0
        self._V = 0
        self._EV = [0 for _ in range(e_range)]
        self._IV = [0 for _ in range(i_range)]
        self._QV = [0 for _ in range(q_range)]
        self._RV = 0
        self._neighbours = list()
        self.move_probability = 0.8
        self.neighbours_move_probability = 0.95
        self.arrived_infected = 0

    def move_lists_stats(self, **kwargs):
        """Method to move people into next stages just to enable changing states"""
        symbol_by_atr = {'E': self._E, 'I': self._I, 'Q': self._Q, 'E2': self._E2, 'I2': self._I2, 'Q2': self._Q2,
                         'EV': self._EV, 'IV': self._IV, 'QV': self._QV}

        for key, val in kwargs.items():
            if key in symbol_by_atr:
                self.move_list_stats(symbol_by_atr[key], val)

    @staticmethod
    def move_list_stats(list_to_update: list[int], new_in_state: int):
        """
        Method to move people in one list
        :param list_to_update: state list with stages (ex. self._I)
        :param new_in_state: number of people joining this state
        """
        list_to_update[-1] += list_to_update[-2]
        for i in range(len(list_to_update) - 3, -1, -1):
            list_to_update[i + 1] = list_to_update[i]

        list_to_update[0] = new_in_state

    def simulate(self):
        """Simulate next day"""
        self._model.simulate()

    def new_cases(self):
        """Num of new cases getter"""
        return self._E[0] + self._E2[0] + self._EV[0]

    def all_exposed(self):
        """Num of exposed people getter"""
        return sum(self._E) + sum(self._E2) + sum(self._EV)

    def all_infected(self):
        """Num of infected people getter"""
        return sum(self._I) + sum(self._I2) + sum(self._IV)

    def all_quarantined(self):
        """Num of quarantined people getter"""
        return sum(self._Q) + sum(self._Q2) + sum(self._QV)

    def all_recovered(self):
        """Num of recovered people getter"""
        return self._R + self._R2 + self._RV

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
    def EV(self):
        return self._EV

    @EV.setter
    def EV(self, value):
        self._EV = value

    @property
    def I(self):
        return self._I

    @I.setter
    def I(self, value):
        self._I = value

    @property
    def I2(self):
        return self._I2

    @I2.setter
    def I2(self, value):
        self._I2 = value

    @property
    def IV(self):
        return self._IV

    @IV.setter
    def IV(self, value):
        self._IV = value

    @property
    def Q(self):
        return self._Q

    @Q.setter
    def Q(self, value):
        self._Q = value

    @property
    def Q2(self):
        return self._Q2

    @Q2.setter
    def Q2(self, value):
        self._Q2 = value

    @property
    def QV(self):
        return self._QV

    @QV.setter
    def QV(self, value):
        self._QV = value

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
    def RV(self):
        return self._RV

    @RV.setter
    def RV(self, value):
        self._RV = value

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, value):
        self._V = value

    @property
    def D(self):
        return self._D

    @D.setter
    def D(self, value):
        self._D = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_class):
        self._model = model_class(self)

    @property
    def neighbours(self):
        return self._neighbours

    @neighbours.setter
    def neighbours(self, value):
        self._neighbours = value
