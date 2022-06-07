from statistics.statistics_seiqrd2 import StatisticsSEIQRD2

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
        self.vaccinated_cnt += point.V + sum(point.EV) + sum(point.IV) + point.RV

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.vaccinated_cnt, self.recovered_and_vaccinated]

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {"vaccinated": f"vaccinated: {self.vaccinated_cnt}",
                                 "recovered_v": f"recovered v: {self.recovered_and_vaccinated}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations

    def generate_plot(self, idx: int, *args) -> None:
        super().generate_plot(idx, *args, 'Vaccinated')
