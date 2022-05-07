from point import Point
from scipy.integrate import solve_ivp
import numpy as np

beta = 0.45
sigma = 0.1
gamma = 0.1

def simulate(point: Point):
    """Func to simulate point"""
    n = point.N + point.arrived_infected
    s, e, i, r = [val / n for val in (point.S, point.E, point.I + point.arrived_infected, point.R)]

    new_s = point.S - beta*i*s
    new_e = point.E + (beta * i * s - sigma * e)
    new_i = sigma * e - gamma * i
    new_r = gamma * i

    point.S, point.E, point.I, point.R = new_s, new_e, new_i, new_r
