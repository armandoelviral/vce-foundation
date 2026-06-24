from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotRecord:
    snapshot_id: str
    state_root: str
    epoch: int

    def __post_init__(self):
        if not self.snapshot_id:
            raise ValueError("snapshot_id is required")

        if not self.state_root:
            raise ValueError("state_root is required")

        if self.epoch <= 0:
            raise ValueError("epoch must be positive")
