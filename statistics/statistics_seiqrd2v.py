from statistics.statistics_seiqrd2 import StatisticsSEIQRD2
import pandas as pd
from matplotlib import pyplot as plt

from logic.models import GenericModel
from logic.point import Point


class StatisticsSEIQRD2V(StatisticsSEIQRD2):
    def __init__(self, model: GenericModel):
        super().__init__(model)
        self.recovered_and_vaccinated = 0
        self.vaccinated_cnt = 0
        self.fieldnames += ["Vaccinated", "Recovered V"]
        self.save_field_names()

    def reset_statistics(self) -> None:
        super().reset_statistics()
        self.recovered_and_vaccinated = 0
        self.vaccinated_cnt = 0

    def update_statistics(self, point: Point) -> None:
        super().update_statistics(point)
        self.recovered_and_vaccinated += point.RV
        self.vaccinated_cnt += point.V

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.vaccinated_cnt, self.recovered_and_vaccinated]

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {"vaccinated": f"vaccinated: {self.vaccinated_cnt}",
                                 "recovered_v": f"recovered v: {self.recovered_and_vaccinated}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations

    def generate_plot(self, idx: int) -> None:
        """Method generating new statistics plot and removing old one"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        data = pd.read_csv('statistics/data.csv')
        day = data['Day']
        new_cases = data['New cases']
        exposed = data['Exposed']
        infective = data['Infected']
        recovered = data['Recovered']
        quarantined = data['Quarantined']
        deaths = data['Deaths']
        recovered_2 = data['Recovered 2']
        vaccinated = data['Vaccinated']
        recovered_v = data['Recovered V']

        ax1.plot(day, exposed, label='Exposed')
        ax1.plot(day, infective, label='Infected')
        ax1.plot(day, recovered, label='Recovered')
        ax1.plot(day, quarantined, label='Quarantined')
        ax1.plot(day, deaths, label='Deaths')
        ax1.plot(day, recovered_2, label='Recovered 2')
        ax1.plot(day, vaccinated, label='Vaccinated')
        ax1.plot(day, recovered_v, label='Recovered V')

        ax1.legend(loc='upper left')

        ax2.plot(day, new_cases, label='New cases')
        ax2.legend(loc='upper left')

        self.save_plot(idx)
