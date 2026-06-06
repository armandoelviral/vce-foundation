from dataclasses import dataclass


@dataclass(frozen=True)
class SignedSnapshotAttestation:

    sequence: int
    state_hash: str
    signature: str
