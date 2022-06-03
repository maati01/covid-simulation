import csv
import os

import pandas as pd
from matplotlib import pyplot as plt

from logic.models import *
from logic.point import Point


class Statistics:
    def __init__(self, model: GenericModel):
        self.model = model
        self.day = 0
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0
        self.vaccinated_cnt = 0
        self.quarantine_cnt = 0
        self.deaths = 0
        self.new_cases = 0

        self.fieldnames = ["Day", "Susceptible", "Exposed", "Infected", "Recovered", "New cases", "Quarantined", "Deaths", "Vaccinated"]
        with open('statistics/data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()

        if not os.path.exists('data/plot'):
            os.mkdir('data/plot')

    def update_data_file(self) -> None:
        with open('statistics/data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            info = {
                "Day": self.day,
                "Susceptible": self.susceptible_cnt,
                "Exposed": self.exposed_cnt,
                "Infected": self.infected_cnt,
                "Recovered": self.recovered_cnt,
                "New cases": self.new_cases,
                "Quarantined": self.quarantine_cnt,
                "Deaths": self.deaths,
                "Vaccinated": self.vaccinated_cnt
            }

            csv_writer.writerow(info)

    def get_statistics(self) -> tuple[str, str, str, str, str, str, str, str, str]:
        return f"Day: {self.day}", f"susceptible: {self.susceptible_cnt}", f"exposed: {self.exposed_cnt}", \
               f"infected: {self.infected_cnt}", f"recovered: {self.recovered_cnt}", f"new cases: {self.new_cases}",\
               f"quarantined: {self.quarantine_cnt}", f"deaths: {self.deaths}", f"vaccinated: {self.vaccinated_cnt}"

    def update_day(self):
        self.day += 1

    def update_statistics(self, point: Point) -> None:
        self.susceptible_cnt += point.S
        self.exposed_cnt += point.all_exposed()
        self.infected_cnt += point.all_infected()
        self.recovered_cnt += point.R
        self.new_cases += point.E[0]
        self.quarantine_cnt += point.all_quarantined()
        self.deaths += point.D
        self.vaccinated_cnt += point.V

    def reset_counters(self) -> None:
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0
        self.new_cases = 0
        self.quarantine_cnt = 0
        self.deaths = 0
        self.vaccinated_cnt = 0

    @staticmethod
    def generate_plot(idx: int) -> None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        data = pd.read_csv('statistics/data.csv')
        day = data['Day']
        new_cases = data['New cases']
        exposed = data['Exposed']
        infective = data['Infected']
        recovered = data['Recovered']
        quarantined = data['Quarantined']
        deaths = data['Deaths']
        vaccinated = data['Vaccinated']

        ax1.plot(day, exposed, label='Exposed')
        ax1.plot(day, infective, label='Infected')
        ax1.plot(day, recovered, label='Recovered')
        ax1.plot(day, quarantined, label='Quarantined')
        ax1.plot(day, deaths, label='Deaths')
        ax1.plot(day, vaccinated, label='Vaccinated')

        ax1.legend(loc='upper left')

        ax2.plot(day, new_cases, label='New cases')
        ax2.legend(loc='upper left')

        if idx != 0:
            os.remove(f"data/plot/plot{idx - 1}.png")
        plt.savefig(f"data/plot/plot{idx}.png")
        plt.close('all')
