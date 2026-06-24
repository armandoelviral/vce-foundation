from dataclasses import dataclass


@dataclass(frozen=True)
class ExpirationRecord:
    expiration_id: str
    trust_id: str
    remaining_days: int

    def __post_init__(self):
        if not self.expiration_id:
            raise ValueError("expiration_id is required")

        if not self.trust_id:
            raise ValueError("trust_id is required")
