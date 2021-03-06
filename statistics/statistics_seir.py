from logic.models import GenericModel
from logic.point import Point
from statistics.statistics import Statistics


class StatisticsSEIR(Statistics):
    def __init__(self, model: GenericModel):
        super().__init__(model)
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0
        self.new_cases = 0
        self.fieldnames += ["Susceptible", "Exposed", "Infected", "Recovered", "New cases"]
        self.save_field_names()

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.susceptible_cnt, self.exposed_cnt, self.infected_cnt,
                                                 self.recovered_cnt, self.new_cases]

    def update_statistics(self, point: Point) -> None:
        """Method updating statistics by adding point's values"""
        self.susceptible_cnt += point.S
        self.exposed_cnt += point.all_exposed()
        self.infected_cnt += point.all_infected()
        self.recovered_cnt += point.R
        self.new_cases += point.new_cases()

    def reset_statistics(self) -> None:
        """Method setting statistic to 0"""
        self.susceptible_cnt = 0
        self.exposed_cnt = 0
        self.infected_cnt = 0
        self.recovered_cnt = 0
        self.new_cases = 0

    def generate_plot(self, idx: int, *args):
        super().generate_plot(idx, *args, 'Exposed', 'Infected', 'Recovered')

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {
            "susceptible": f"susceptible: {self.susceptible_cnt}",
            "exposed": f"exposed: {self.exposed_cnt}",
            "infected": f"infected: {self.infected_cnt}",
            "recovered": f"recovered: {self.recovered_cnt}",
            "new_cases": f"new cases: {self.new_cases}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations
