from statistics.statistics_seiqr import StatisticsSEIQR

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
        stats_representations = {"deaths": f"deaths: {self.deaths}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations

    def generate_plot(self, idx: int, *args) -> None:
        super().generate_plot(idx, *args, 'Deaths')
