from dataclasses import dataclass
from enum import StrEnum


class RuleObservationStatus(StrEnum):
    """Observed outcome for one customer-defined retail rule."""

    CONFORMANT = "CONFORMANT"
    NON_CONFORMANT = "NON_CONFORMANT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True, slots=True)
class RetailContextRuleObservation:
    """Immutable retail rule observation with opaque evidence references."""

    observation_id: str
    rule_id: str
    snapshot_id: str
    snapshot_version: int
    case_id: str
    status: RuleObservationStatus
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        identity_fields = {
            "observation_id": self.observation_id,
            "rule_id": self.rule_id,
            "snapshot_id": self.snapshot_id,
            "case_id": self.case_id,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(identity, str)
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if (
            isinstance(self.snapshot_version, bool)
            or not isinstance(self.snapshot_version, int)
            or self.snapshot_version < 1
        ):
            raise ValueError(
                "snapshot_version must be a positive integer"
            )

        if not isinstance(
            self.status,
            RuleObservationStatus,
        ):
            raise TypeError(
                "status must be a RuleObservationStatus"
            )

        if not isinstance(
            self.evidence_ids,
            tuple,
        ):
            raise TypeError(
                "evidence_ids must be an immutable tuple"
            )

        conclusive_statuses = {
            RuleObservationStatus.CONFORMANT,
            RuleObservationStatus.NON_CONFORMANT,
        }

        if (
            self.status in conclusive_statuses
            and not self.evidence_ids
        ):
            raise ValueError(
                "conclusive observation requires evidence"
            )

        seen_ids: set[str] = set()

        for evidence_id in self.evidence_ids:
            if (
                not isinstance(evidence_id, str)
                or not evidence_id.strip()
            ):
                raise ValueError(
                    "evidence_id must not be empty"
                )

            if evidence_id in seen_ids:
                raise ValueError(
                    "duplicate evidence_id: "
                    f"{evidence_id}"
                )

            seen_ids.add(
                evidence_id
            )
