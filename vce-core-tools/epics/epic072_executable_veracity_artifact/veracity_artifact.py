from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VeracityArtifact:
    identity: dict[str, Any]
    trust: dict[str, Any]
    provenance: dict[str, Any]
    replay: dict[str, Any]
    evidence: dict[str, Any]
    governance: dict[str, Any]

    def to_dict(self):

        return {
            "identity": self.identity,
            "trust": self.trust,
            "provenance": self.provenance,
            "replay": self.replay,
            "evidence": self.evidence,
            "governance": self.governance,
        }
