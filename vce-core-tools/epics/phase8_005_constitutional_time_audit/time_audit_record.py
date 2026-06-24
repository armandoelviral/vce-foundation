from dataclasses import dataclass


@dataclass(frozen=True)
class TimeAuditRecord:
    audit_id: str
    snapshot_id: str
    epoch: int

    def __post_init__(self):
        if not self.audit_id:
            raise ValueError("audit_id is required")

        if not self.snapshot_id:
            raise ValueError("snapshot_id is required")

        if self.epoch <= 0:
            raise ValueError("epoch must be positive")
