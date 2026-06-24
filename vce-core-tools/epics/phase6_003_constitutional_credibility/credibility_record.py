from dataclasses import dataclass


@dataclass(frozen=True)
class CredibilityRecord:
    credibility_id: str
    identity_id: str
    credibility_delta: int

    def __post_init__(self):
        if not self.credibility_id:
            raise ValueError("credibility_id is required")

        if not self.identity_id:
            raise ValueError("identity_id is required")
