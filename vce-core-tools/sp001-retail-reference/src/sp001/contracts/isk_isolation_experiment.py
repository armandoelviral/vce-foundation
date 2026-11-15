from dataclasses import dataclass
from enum import StrEnum


class IsolationPlatform(StrEnum):
    MACOS = "MACOS"
    LINUX = "LINUX"


@dataclass(frozen=True, slots=True)
class IsolationExperiment:
    """Immutable experiment identity; grants no execution authority."""

    experiment_id: str
    platform: IsolationPlatform
    invariant_id: str
    threat_model_id: str
    resource_id: str
    attempt_id: str

    def __post_init__(self) -> None:
        identities = {
            "experiment_id": self.experiment_id,
            "invariant_id": self.invariant_id,
            "threat_model_id": self.threat_model_id,
            "resource_id": self.resource_id,
            "attempt_id": self.attempt_id,
        }

        for name, value in identities.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")

        if not isinstance(self.platform, IsolationPlatform):
            raise TypeError("platform must be an IsolationPlatform")
