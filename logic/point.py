from SEIR import GenericModel

class Point:
    def __init__(self, init_N: int, model: GenericModel, province: str = None):  # TODO province should be enum I think
        self._N = init_N
        self._province = province
        self._model = model(self)
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

    @property
    def model(self):
        return self._model

    def simulate(self):
        """Simulate next day"""
        self._model.simulate()
