from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotAttestation:

    sequence: int
    state_hash: str
