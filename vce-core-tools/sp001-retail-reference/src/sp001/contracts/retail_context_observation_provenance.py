from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)


@dataclass(frozen=True, slots=True)
class RetailContextObservationProvenance:
    """Immutable source and temporal provenance for one context dimension."""

    observation_id: str
    observation_version: int
    case_id: str
    snapshot_id: str
    snapshot_version: int
    dimension_id: str
    source_identity: KnowledgeSourceIdentity
    observed_at: datetime
    recorded_at: datetime
    effective_from: datetime
    evidence_ids: tuple[str, ...]
    effective_until: datetime | None = None

    def __post_init__(self) -> None:
        identity_fields = {
            "observation_id": self.observation_id,
            "case_id": self.case_id,
            "snapshot_id": self.snapshot_id,
            "dimension_id": self.dimension_id,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        version_fields = {
            "observation_version": self.observation_version,
            "snapshot_version": self.snapshot_version,
        }

        for field, version in version_fields.items():
            if (
                isinstance(
                    version,
                    bool,
                )
                or not isinstance(
                    version,
                    int,
                )
                or version < 1
            ):
                raise ValueError(
                    f"{field} must be a positive integer"
                )

        if not isinstance(
            self.source_identity,
            KnowledgeSourceIdentity,
        ):
            raise TypeError(
                "source_identity must be a "
                "KnowledgeSourceIdentity"
            )

        temporal_fields = {
            "observed_at": self.observed_at,
            "recorded_at": self.recorded_at,
            "effective_from": self.effective_from,
        }

        if self.effective_until is not None:
            temporal_fields[
                "effective_until"
            ] = self.effective_until

        for field, value in temporal_fields.items():
            self._validate_temporal_field(
                field=field,
                value=value,
            )

        if self.recorded_at < self.observed_at:
            raise ValueError(
                "recorded_at must not be before observed_at"
            )

        if self.observed_at < self.effective_from:
            raise ValueError(
                "observed_at must not be before effective_from"
            )

        if self.effective_until is not None:
            if self.effective_until <= self.effective_from:
                raise ValueError(
                    "effective_until must be after effective_from"
                )

            if self.observed_at >= self.effective_until:
                raise ValueError(
                    "observed_at must be before effective_until"
                )

        if not isinstance(
            self.evidence_ids,
            tuple,
        ):
            raise TypeError(
                "evidence_ids must be an immutable tuple"
            )

        if not self.evidence_ids:
            raise ValueError(
                "evidence_ids must not be empty"
            )

        seen_evidence_ids: set[str] = set()

        for evidence_id in self.evidence_ids:
            if (
                not isinstance(
                    evidence_id,
                    str,
                )
                or not evidence_id.strip()
            ):
                raise ValueError(
                    "evidence_id must not be empty"
                )

            if evidence_id in seen_evidence_ids:
                raise ValueError(
                    "duplicate evidence_id: "
                    f"{evidence_id}"
                )

            seen_evidence_ids.add(
                evidence_id,
            )

    @staticmethod
    def _validate_temporal_field(
        *,
        field: str,
        value: object,
    ) -> None:
        if not isinstance(
            value,
            datetime,
        ):
            raise TypeError(
                f"{field} must be a datetime"
            )

        if (
            value.tzinfo is None
            or value.utcoffset() is None
        ):
            raise ValueError(
                f"{field} must be timezone-aware"
            )
