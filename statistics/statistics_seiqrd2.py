from logic.models import GenericModel
from logic.point import Point
from statistics.statistics_seqird import StatisticsSEIQRD


class StatisticsSEIQRD2(StatisticsSEIQRD):
    def __init__(self, model: GenericModel):
        super().__init__(model)
        self.recovered_second_time = 0
        self.fieldnames += ["Recovered 2"]
        self.save_field_names()

    def reset_statistics(self) -> None:
        super().reset_statistics()
        self.recovered_second_time = 0

    def update_statistics(self, point: Point) -> None:
        super().update_statistics(point)
        self.recovered_second_time += point.R2

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.recovered_second_time]

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {"recovered_second_time": f"recovered 2: {self.recovered_second_time}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations
