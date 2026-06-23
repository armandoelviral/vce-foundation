from dataclasses import dataclass


@dataclass(frozen=True)
class LiabilityBoundary:

    liability_cap: int
    consequential_damages_excluded: bool
    lost_profit_excluded: bool

    def to_dict(self):

        return {
            "liability_cap": self.liability_cap,
            "consequential_damages_excluded":
                self.consequential_damages_excluded,
            "lost_profit_excluded":
                self.lost_profit_excluded,
        }
