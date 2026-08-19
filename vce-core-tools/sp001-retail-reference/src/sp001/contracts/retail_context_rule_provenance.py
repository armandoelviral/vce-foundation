from dataclasses import dataclass
from enum import StrEnum


class RuleProvenanceType(StrEnum):
    """Evidence relationship supporting a retail rule observation."""

    DIRECTLY_OBSERVED = "DIRECTLY_OBSERVED"
    DERIVED = "DERIVED"


@dataclass(frozen=True, slots=True)
class RetailContextRuleProvenance:
    """Immutable provenance declaration for one retail rule."""

    rule_id: str
    provenance_type: RuleProvenanceType
    source_rule_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not isinstance(self.rule_id, str)
            or not self.rule_id.strip()
        ):
            raise ValueError(
                "rule_id must not be empty"
            )

        if not isinstance(
            self.provenance_type,
            RuleProvenanceType,
        ):
            raise TypeError(
                "provenance_type must be a "
                "RuleProvenanceType"
            )

        if not isinstance(
            self.source_rule_ids,
            tuple,
        ):
            raise TypeError(
                "source_rule_ids must be an immutable tuple"
            )

        if (
            self.provenance_type
            is RuleProvenanceType.DERIVED
            and not self.source_rule_ids
        ):
            raise ValueError(
                "derived provenance requires source rules"
            )

        if (
            self.provenance_type
            is RuleProvenanceType.DIRECTLY_OBSERVED
            and self.source_rule_ids
        ):
            raise ValueError(
                "directly observed provenance "
                "cannot declare source rules"
            )

        seen_ids: set[str] = set()

        for source_rule_id in self.source_rule_ids:
            if (
                not isinstance(source_rule_id, str)
                or not source_rule_id.strip()
            ):
                raise ValueError(
                    "source rule_id must not be empty"
                )

            if source_rule_id == self.rule_id:
                raise ValueError(
                    "derived rule cannot depend on itself: "
                    f"{self.rule_id}"
                )

            if source_rule_id in seen_ids:
                raise ValueError(
                    "duplicate source rule_id: "
                    f"{source_rule_id}"
                )

            seen_ids.add(
                source_rule_id
            )
