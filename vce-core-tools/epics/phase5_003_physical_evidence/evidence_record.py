from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    observation_id: str
    evidence_type: str
    artifact_hash: str

    def __post_init__(self):
        if not self.evidence_id:
            raise ValueError("evidence_id is required")

        if not self.observation_id:
            raise ValueError("observation_id is required")

        if not self.evidence_type:
            raise ValueError("evidence_type is required")

        if not self.artifact_hash:
            raise ValueError("artifact_hash is required")
