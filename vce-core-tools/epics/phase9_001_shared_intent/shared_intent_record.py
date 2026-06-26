from dataclasses import dataclass


@dataclass(frozen=True)
class SharedIntentRecord:
    intent_id: str
    purpose: str
    participants: int

    def __post_init__(self):
        if not self.intent_id:
            raise ValueError("intent_id is required")

        if not self.purpose:
            raise ValueError("purpose is required")

        if self.participants <= 0:
            raise ValueError("participants must be positive")
