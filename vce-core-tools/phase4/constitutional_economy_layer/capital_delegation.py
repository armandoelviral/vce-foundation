from dataclasses import dataclass


@dataclass(frozen=True)
class CapitalDelegation:

    delegator_id: str
    delegate_id: str
    amount: int

    def to_dict(self):

        return {
            "delegator_id": self.delegator_id,
            "delegate_id": self.delegate_id,
            "amount": self.amount,
        }
