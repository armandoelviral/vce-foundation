from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SignedArtifact:
    artifact_hash: str
    signature: str
    signer: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "artifact_hash": self.artifact_hash,
            "signature": self.signature,
            "signer": self.signer,
        }
