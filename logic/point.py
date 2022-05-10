class Point:
    def __init__(self, init_N: int, x: int, y: int, province: str = None):  # TODO province should be enum I think
        self.x = x
        self.y = y
        self._N = init_N
        self._province = province
        self._model = None
        self._S = init_N
        self._E = 0
        self._I = 0
        self._R = 0
        self.neighbours = list()
        self.move_probability = 0.5
        self.neighbours_move_probability = 0.7
        self.arrived_infected = 0
        self._points_sorted_by_distance = None

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

    @model.setter
    def model(self, model_class):
        self._model = model_class(self)

    @property
    def points_sorted_by_distance(self):
        return self._points_sorted_by_distance

    @points_sorted_by_distance.setter
    def points_sorted_by_distance(self, sorted_points):
        self._points_sorted_by_distance = sorted_points

    def simulate(self):
        """Simulate next day"""
        self._model.simulate()
