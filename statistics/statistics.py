from abc import ABC, abstractmethod

import pandas as pd
from matplotlib import pyplot as plt
from logic.models import GenericModel
from logic.point import Point
import csv
import os
import re

PLOT_DIR = os.path.join('data', 'plot')
DATA_CSV_PATH = os.path.join('statistics', 'data.csv')


class Statistics(ABC):
    """Abstract class to handle simulation statistics"""

    def __init__(self, model: GenericModel):
        self.model = model
        self.day = 0
        self.fieldnames = ["Day"]

    def update_day(self):
        """Method updating day counter"""
        self.day += 1

    def get_attributes_array(self):
        return [self.day]

    def save_field_names(self) -> None:
        with open('statistics/data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()

        if not os.path.exists(PLOT_DIR):
            os.mkdir(PLOT_DIR)
        else:
            for filename in filter(lambda f: re.match(r'plot\d+\.png', f), os.listdir(PLOT_DIR)):
                os.remove(os.path.join(PLOT_DIR, filename))

    def generate_plot(self, idx: int, *args) -> None:
        """Method generating new statistics plot and removing old one"""

        statistics_name = ['Exposed', 'Infected', 'Recovered', 'Quarantined', 'Deaths', 'Recovered 2', 'Vaccinated',
                           'Recovered V']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        data = pd.read_csv('statistics/data.csv')
        day = data['Day']

        for arg in args:
            if arg in statistics_name:
                ax1.plot(day, data[arg], label=arg)

        ax1.legend(loc='upper left')

        ax2.plot(day, data['New cases'], label='New cases')
        ax2.legend(loc='upper left')

        if idx != 0:
            os.remove(os.path.join(PLOT_DIR, f"plot{idx - 1}.png"))
        plt.savefig(f"data/plot/plot{idx}.png")
        plt.close('all')

    @abstractmethod
    def reset_statistics(self) -> None:
        """Method setting statistic to 0"""

    @abstractmethod
    def update_statistics(self, point: Point) -> None:
        """Method updating statistics by adding point's values"""

    def update_data_file(self) -> None:
        """Method to add new stats to csv data file"""
        info = dict(zip(self.fieldnames, self.get_attributes_array()))
        with open(DATA_CSV_PATH, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writerow(info)

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {
            "day": f"Day: {self.day}"}
        return stats_representations
