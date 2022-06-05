from statistics.statistics_seiqr import StatisticsSEIQR
import pandas as pd
from matplotlib import pyplot as plt

from logic.models import GenericModel
from logic.point import Point


class StatisticsSEIQRD(StatisticsSEIQR):
    def __init__(self, model: GenericModel):
        super().__init__(model)
        self.deaths = 0
        self.fieldnames += ["Deaths"]
        self.save_field_names()

    def reset_statistics(self) -> None:
        super().reset_statistics()
        self.deaths = 0

    def update_statistics(self, point: Point) -> None:
        super().update_statistics(point)
        self.deaths += point.D

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.deaths]

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {
            "day": f"Day: {self.day}",
            "susceptible": f"susceptible: {self.susceptible_cnt}",
            "exposed": f"exposed: {self.exposed_cnt}",
            "infected": f"infected: {self.infected_cnt}",
            "recovered": f"recovered: {self.recovered_cnt}",
            "new_cases": f"new cases: {self.new_cases}",
            "quarantined": f"quarantined: {self.quarantine_cnt}",
            "deaths": f"deaths: {self.deaths}",
        }
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

        ax1.plot(day, exposed, label='Exposed')
        ax1.plot(day, infective, label='Infected')
        ax1.plot(day, recovered, label='Recovered')
        ax1.plot(day, quarantined, label='Quarantined')
        ax1.plot(day, deaths, label='Deaths')

        ax1.legend(loc='upper left')

        ax2.plot(day, new_cases, label='New cases')
        ax2.legend(loc='upper left')

        self.save_plot(idx)
