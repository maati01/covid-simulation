from logic.point import Point
from abc import ABC, abstractmethod
from math import ceil, floor
import random


# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7277829/#:~:text=The%20classical%20SEIR%20model%20can%20be%20described%20by%20a%20series%20of%20ordinary%20differential%20equations%3A
# http://web.pdx.edu/~gjay/teaching/mth271_2020/html/09_SEIR_model.html
class GenericModel(ABC):
    """Abstract class for COVID simulation models"""

    def __init__(self, point: Point):
        self._point = point

    @abstractmethod
    def update_data(self):
        """Abstract method to update point data"""
        pass

    @abstractmethod
    def simulate(self):
        """Abstract method to simulate point"""
        pass

    def get_moving_infected_people(self):
        """Number of infected people moving to and outside neighbours getter"""
        infected_to_move = round(self._point.all_infected() * random.uniform(0.01, 0.3))

        infected_to_neighbours = round(infected_to_move * self._point.neighbours_move_probability)
        infected_out_neighbours = infected_to_move - infected_to_neighbours

        rand = random.random()
        if rand > 0.5:
            infected_out_neighbours = 0
        elif rand > 0.1:
            infected_out_neighbours = round(infected_out_neighbours * random.uniform(0, 0.7))

        return infected_to_neighbours, infected_out_neighbours

    @staticmethod
    def _reduce_stages(list_to_update: list[int], vals: list[int]):
        """
        Method to reduce stages in given list by given vals
        :param list_to_update: stages list (ex. self._point.I)
        :param vals: values to subtract from `list_to_update`
        :return: updated `list_to_update`
        """
        updated_list = list()
        for (stage, val) in zip(list_to_update, vals):
            updated_list.append(stage - val)

        return updated_list

    @staticmethod
    def _get_round_func():
        """Method to randomly get rounding function (floor or ceil)"""
        return random.choice((floor, ceil))


class SEIR(GenericModel):
    """
    Class created for simulating COVID with SEIR model

    S - susceptible
    E - exposed (cannot infect others)
    I - infected (can infect others)
    R - recovered

    MODEL PATH:
    S --> E --> I --> R
    """
    kappa = 0.7  # for getting recovered
    gamma = 0.4  # for getting infected
    beta = 0.72  # for getting exposed

    def __init__(self, point: Point):
        super().__init__(point)
        self.i_able_to_recover = 0
        self.e_able_to_infected = 0
        self.n = 0
        self.i = 0
        self.s_div_n = 0
        self.round_func = None

    def update_data(self):
        """Method to update values needed to simulate COVID with SEIR model"""
        self.i_able_to_recover = self._point.I[-1]
        self.e_able_to_infected = self._point.E[-1]
        self.n = self._point.N + self._point.arrived_infected
        self.i = self._point.all_infected() + self._point.arrived_infected
        self.s_div_n = self._point.S / self.n
        self.round_func = self._get_round_func()

    def simulate(self):
        """Method to simulate point with SEIR model"""
        beta_i_s_div_n, gamma_e, kappa_i = (
            self.round_func(self.beta * self.i * self.s_div_n),
            self.round_func(self.gamma * self.e_able_to_infected),
            self.round_func(self.kappa * self.i_able_to_recover)
        )

        self._point.S -= beta_i_s_div_n
        self._point.E[-1] -= gamma_e
        self._point.I[-1] -= kappa_i
        self._point.R += kappa_i
        self._point.move_lists_stats(E=beta_i_s_div_n, I=gamma_e)

        self._point.arrived_infected = 0


class SEIQR(SEIR):
    """
    Class created for simulating COVID with SEIQR model

    S - susceptible
    E - exposed (cannot infect others)
    I - infected (can infect others)
    Q - quarantined
    R - recovered

    MODEL PATH:
    S --> E --> I -----------> R
                 \      /
                  ---> Q
    """
    alpha = 0.05  # for getting quarantined

    def __init__(self, point: Point):
        super().__init__(point)
        self.q_able_to_recover = 0

    def update_data(self):
        """Method to update values need to simulate COVID with SEIQR model"""
        super().update_data()
        self.q_able_to_recover = self._point.Q[-1]

    def simulate(self):
        """Method to simulate point with SEIQR model"""
        kappa_q = self.round_func(self.kappa * self.q_able_to_recover)
        q_from_i_per_stage = [round(self.alpha * stage) for stage in self._point.I]

        super().simulate()

        self._point.I = self._reduce_stages(self._point.I, q_from_i_per_stage)
        self._point.Q[-1] -= kappa_q
        self._point.R += kappa_q
        self._point.move_lists_stats(Q=sum(q_from_i_per_stage))


class SEIQRD(SEIQR):
    """
    Class created for simulating COVID with SEIQRD model

    S - susceptible
    E - exposed (cannot infect others)
    I - infected (can infect others)
    Q - quarantined
    R - recovered
    D - deaths

    MODEL PATH:
    S --> E --> I ----------> R
                 \      /
                  ---> Q
                        \
                         ---> D
    """
    theta = 0.01  # for getting dead

    def update_data(self):
        """Method to update values need to simulate COVID with SEIQRD model"""
        super().update_data()

    def simulate(self):
        """Method to simulate point with SEIQRD model"""
        d_from_q_per_stage = [round(self.theta * stage) for stage in self._point.Q]

        super().simulate()

        self._point.Q = self._reduce_stages(self._point.Q, d_from_q_per_stage)
        self._point.D += sum(d_from_q_per_stage)


class SEIQRD2(SEIQRD):
    """
    Class created for simulating COVID with SEIQRD2 model.
    It is almost the same as SEIQRD model, but with double infection possibility.

    S - susceptible
    E - exposed (cannot infect others)
    I - infected (can infect others)
    Q - quarantined
    R - recovered
    D - deaths
    E2 - exposed second time (cannot infect others)
    I2 - infected second time(can infect others)
    Q2 - quarantined second time
    R2 - recovered second time (cannot be infected again)

    MODEL PATH:
    S --> E --> I ----------> R --> E2 --> I2 -----------> R2
                 \      /                    \       /
                  ---> Q                       ---> Q2
                        \                          /
                         ----------> D <-----------
    """
    beta2 = 0.005  # for getting exposed second time

    def __init__(self, point: Point):
        super().__init__(point)
        self.i_able_to_recover2 = 0
        self.e_able_to_infected2 = 0
        self.q_able_to_recover2 = 0
        self.r_div_n = 0

    def update_data(self):
        """Method to update values need to simulate COVID with SEIQRD2 model"""
        super().update_data()
        self.i_able_to_recover2 = self._point.I2[-1]
        self.e_able_to_infected2 = self._point.E2[-1]
        self.q_able_to_recover2 = self._point.Q2[-1]
        self.r_div_n = self._point.R / self.n

    def simulate(self):
        """Method to simulate point with SEIQRD2 model"""
        beta_i_r_div_n, gamma_e2, kappa_i2, kappa_q2 = (
            min(self.round_func(self.beta2 * self.i * self.r_div_n), self._point.R),
            self.round_func(self.gamma * self.e_able_to_infected2),
            self.round_func(self.kappa * self.i_able_to_recover2),
            self.round_func(self.kappa * self.q_able_to_recover2)
        )

        q2_from_i2_per_stage = [round(self.alpha * stage) for stage in self._point.I2]
        d_from_q2_per_stage = [round(self.theta * stage) for stage in self._point.Q2]

        super().simulate()

        self._point.Q2 = self._reduce_stages(self._point.Q2, d_from_q2_per_stage)
        self._point.I2 = self._reduce_stages(self._point.I2, q2_from_i2_per_stage)

        self._point.R -= beta_i_r_div_n
        self._point.E2[-1] -= gamma_e2
        self._point.I2[-1] -= kappa_i2
        self._point.Q2[-1] -= kappa_q2
        self._point.R2 += (kappa_q2 + kappa_i2)
        self._point.D += sum(d_from_q2_per_stage)

        self._point.move_lists_stats(E2=beta_i_r_div_n, I2=gamma_e2, Q2=sum(q2_from_i2_per_stage))


class SEIQRD2V(SEIQRD2):
    """
    Class created for simulating COVID with SEIQRD2V model.
    It is almost the same as SEIQRD2 model, but vaccination is added.

    S - susceptible
    E - exposed (cannot infect others)
    I - infected (can infect others)
    Q - quarantined
    R - recovered
    D - deaths
    E2 - exposed second time (cannot infect others)
    I2 - infected second time(can infect others)
    Q2 - quarantined second time
    R2 - recovered second time (cannot be infected again)
    V - vaccinated
    EV - exposed and vaccinated (cannot infect others)
    IV - infected and vaccinated (can infect others)
    QV - quarantined and vaccinated (cannot die)
    RV - recovered and vaccinated (cannot be infected again)

    MODEL PATH:
    S --> E --> I ----------> R --> E2 --> I2 -----------> R2
    |            \      /     |               \       /
    |             ---> Q      |                ---> Q2
    |                   \     |                    /
    |                    ----------> D <-----------
    |                         |
    -----------------------------> V --> EV --> IV --------------> RV
                                                 \       /
                                                  ---> QV
    """
    betaV = 0.001  # for getting exposed being vaccinated
    omega = 0  # for getting vaccinated

    def __init__(self, point: Point):
        super().__init__(point)
        self.i_able_to_recoverV = 0
        self.e_able_to_infectedV = 0
        self.q_able_to_recoverV = 0
        self.v_div_n = 0

    def update_data(self):
        """Method to update values need to simulate COVID with SEIQRD2V model"""
        super().update_data()
        self.i_able_to_recoverV = self._point.IV[-1]
        self.e_able_to_infectedV = self._point.EV[-1]
        self.q_able_to_recoverV = self._point.QV[-1]
        self.v_div_n = self._point.V / self.n

    def simulate(self):
        """Method to simulate point with SEIQRD2V model"""
        beta_i_v_div_n, gamma_eV, kappa_iV, kappa_qV = (
            min(self.round_func(self.betaV * self.i * self.v_div_n), self._point.V),
            self.round_func(self.gamma * self.e_able_to_infectedV),
            self.round_func(self.kappa * self.i_able_to_recoverV),
            self.round_func(self.kappa * self.q_able_to_recoverV)
        )

        omega_r, omega_s = floor(self.omega * self._point.R), floor(self.omega * self._point.S)
        qV_from_iV_per_stage = [round(self.alpha * stage) for stage in self._point.IV]

        super().simulate()

        self._point.IV = self._reduce_stages(self._point.IV, qV_from_iV_per_stage)

        self._point.S -= omega_s
        self._point.R -= omega_r
        self._point.V += (omega_r + omega_s - beta_i_v_div_n)
        self._point.EV[-1] -= gamma_eV
        self._point.IV[-1] -= kappa_iV
        self._point.QV[-1] -= kappa_qV
        self._point.RV += (kappa_qV + kappa_iV)

        self._point.move_lists_stats(EV=beta_i_v_div_n, IV=gamma_eV, QV=sum(qV_from_iV_per_stage))