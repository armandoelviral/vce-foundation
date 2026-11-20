from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.product001_host_admission import (
    REQUIRED_CHECK_IDS,
)


HOST_FACT_DOMAIN = b"HOST-FACT-ASSERTION-V1\x00"


class DeclaredHostFactStatus(StrEnum):
    SATISFIED = "SATISFIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class HostFactAssertion:
    """Unverified structural host observation; grants no authority."""

    assertion_id: str
    observer_id: str
    mandate_id: str
    host_id: str
    resource_id: str
    check_id: str
    evaluation_id: str
    challenge_id: str
    nonce: bytes
    observed_at: int
    policy_version: str
    declared_status: DeclaredHostFactStatus
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in (
            "assertion_id",
            "observer_id",
            "mandate_id",
            "host_id",
            "resource_id",
            "check_id",
            "evaluation_id",
            "challenge_id",
            "policy_version",
        ):
            value = getattr(self, field)
            if type(value) is not str or not value.strip():
                raise ValueError(
                    f"{field} must be a nonempty string"
                )

        if self.check_id not in REQUIRED_CHECK_IDS:
            raise ValueError(
                "check_id must belong to HOST-P01..HOST-P10"
            )

        if type(self.nonce) is not bytes:
            raise TypeError("nonce must be bytes")

        if len(self.nonce) != 32:
            raise ValueError("nonce must contain exactly 32 bytes")

        if type(self.observed_at) is not int:
            raise TypeError("observed_at must be an integer")

        if self.observed_at < 0:
            raise ValueError("observed_at must be nonnegative")

        if type(self.declared_status) is not DeclaredHostFactStatus:
            raise TypeError(
                "declared_status must be a DeclaredHostFactStatus"
            )

        if type(self.evidence_ids) is not tuple:
            raise TypeError(
                "evidence_ids must be an immutable tuple"
            )

        seen = set()

        for evidence_id in self.evidence_ids:
            if type(evidence_id) is not str or not evidence_id.strip():
                raise ValueError(
                    "evidence_id must be a nonempty string"
                )

            if evidence_id in seen:
                raise ValueError("duplicate evidence_id")

            seen.add(evidence_id)
