from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceRecord:

    snapshot_hash: str
    parent_hash: str | None
