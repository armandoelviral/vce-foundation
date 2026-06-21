from dataclasses import dataclass


@dataclass(frozen=True)
class TcuEvidenceBlock:

    artifact_hash: str
    facts_hash: str
    input_commitment: str
    purified_time_utc: str

    def to_dict(self):

        return {
            "artifact_hash": self.artifact_hash,
            "facts_hash": self.facts_hash,
            "input_commitment": self.input_commitment,
            "purified_time_utc": self.purified_time_utc,
        }
