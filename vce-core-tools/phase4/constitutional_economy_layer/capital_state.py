from dataclasses import dataclass


@dataclass(frozen=True)
class CapitalState:

    balance: int

    def to_dict(self):

        return {
            "balance": self.balance,
        }
