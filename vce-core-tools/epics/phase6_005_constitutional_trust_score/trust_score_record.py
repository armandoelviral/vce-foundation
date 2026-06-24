from dataclasses import dataclass


@dataclass(frozen=True)
class TrustScoreRecord:
    score_id: str
    identity_id: str
    score: int

    def __post_init__(self):
        if not self.score_id:
            raise ValueError("score_id is required")

        if not self.identity_id:
            raise ValueError("identity_id is required")
