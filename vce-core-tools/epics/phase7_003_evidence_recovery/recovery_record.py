from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryRecord:
    recovery_id: str
    evidence_id: str
    recovery_type: str

    def __post_init__(self):
        if not self.recovery_id:
            raise ValueError("recovery_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")

        if not self.recovery_type:
            raise ValueError("recovery_type is required")
