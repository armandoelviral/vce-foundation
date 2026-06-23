from dataclasses import dataclass


@dataclass(frozen=True)
class CapitalAccrual:

    identity_id: str
    amount: int

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "amount": self.amount,
        }
