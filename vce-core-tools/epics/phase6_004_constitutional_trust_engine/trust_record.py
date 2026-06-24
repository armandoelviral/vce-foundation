from dataclasses import dataclass


@dataclass(frozen=True)
class TrustRecord:
    trust_id: str
    identity_id: str
    trust_delta: int

    def __post_init__(self):
        if not self.trust_id:
            raise ValueError("trust_id is required")

        if not self.identity_id:
            raise ValueError("identity_id is required")
