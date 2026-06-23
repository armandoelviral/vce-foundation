from dataclasses import dataclass


@dataclass(frozen=True)
class CapitalRecord:

    identity_id: str
    capital: int

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "capital": self.capital,
        }
