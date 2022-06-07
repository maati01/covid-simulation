from statistics.statistics_seir import StatisticsSEIR

from logic.models import GenericModel
from logic.point import Point


class StatisticsSEIQR(StatisticsSEIR):
    def __init__(self, model: GenericModel):
        super().__init__(model)
        self.quarantine_cnt = 0
        self.fieldnames += ["Quarantined"]
        self.save_field_names()

    def update_statistics(self, point: Point) -> None:
        super().update_statistics(point)
        self.quarantine_cnt += point.all_quarantined()

    def reset_statistics(self) -> None:
        super().reset_statistics()
        self.quarantine_cnt = 0

    def get_attributes_array(self):
        return super().get_attributes_array() + [self.quarantine_cnt]

    @property
    def current_stats_representations(self) -> dict[str, str]:
        stats_representations = {"quarantined": f"quarantined: {self.quarantine_cnt}"}
        stats_representations.update(super().current_stats_representations)

        return stats_representations

    def generate_plot(self, idx: int, *args) -> None:
        super().generate_plot(idx, *args, 'Quarantined')
