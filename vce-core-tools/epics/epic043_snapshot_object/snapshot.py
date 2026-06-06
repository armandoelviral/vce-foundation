from dataclasses import dataclass


@dataclass(frozen=True)
class Snapshot:

    sequence: int
    state_hash: str
