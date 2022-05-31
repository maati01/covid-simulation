import csv

from logic.point import Point


class Statistics:
    def __init__(self):
        self.fieldnames = ["Day", "Susceptible", "Exposed", "Infected", "Recovered", "New cases"]
        with open('statistics/data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writeheader()

        self.day = 0
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0

        # Statistics from previous day
        self.prev_infected_cnt = 0

        self.new_cases = 0

    def update_data_file(self) -> None:
        with open('statistics/data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            info = {
                "Day": self.day,
                "Susceptible": self.susceptible_cnt,
                "Exposed": self.exposed_cnt,
                "Infected": self.infected_cnt,
                "Recovered": self.recovered_cnt,
                "New cases": self.new_cases
            }

            csv_writer.writerow(info)

    def get_statistics(self) -> tuple[str, str, str, str, str, str]:
        return f"Day: {self.day}", f"susceptible: {self.susceptible_cnt}", f"exposed: {self.exposed_cnt}", \
               f"infected: {self.infected_cnt}", f"recovered: {self.recovered_cnt}", f"new cases: {self.new_cases}"

    def update_day(self):
        self.day += 1

    def update_new_cases(self):
        self.new_cases = max(self.infected_cnt - self.prev_infected_cnt, 0)
        self.prev_infected_cnt = self.infected_cnt

    def update_statistics(self, point: Point) -> None:
        self.susceptible_cnt += point.S
        self.exposed_cnt += point.all_exposed
        self.infected_cnt += point.all_infected
        self.recovered_cnt += point.R

    def reset_counters(self) -> None:
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0
