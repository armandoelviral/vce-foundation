from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class EnvironmentFingerprint:
    container_digest: str
    runtime_version: str
    dependency_manifest_hash: str
    model_fingerprint: str
    policy_version: str
    execution_profile: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "container_digest": self.container_digest,
            "runtime_version": self.runtime_version,
            "dependency_manifest_hash": self.dependency_manifest_hash,
            "model_fingerprint": self.model_fingerprint,
            "policy_version": self.policy_version,
            "execution_profile": self.execution_profile,
        }
