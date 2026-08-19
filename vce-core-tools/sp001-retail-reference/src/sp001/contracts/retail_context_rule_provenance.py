from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
    RetailContextDependencySource,
)


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
    dependency_sources: tuple[
        RetailContextDependencySource,
        ...,
    ] = ()

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

        if not isinstance(
            self.dependency_sources,
            tuple,
        ):
            raise TypeError(
                "dependency_sources must be an immutable tuple"
            )

        if (
            self.provenance_type
            is RuleProvenanceType.DERIVED
            and not self.source_rule_ids
            and not self.dependency_sources
        ):
            raise ValueError(
                "derived provenance requires source rules"
            )

        if (
            self.provenance_type
            is RuleProvenanceType.DIRECTLY_OBSERVED
            and (
                self.source_rule_ids
                or self.dependency_sources
            )
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

        seen_typed_sources: set[
            tuple[DependencySourceType, str]
        ] = set()

        for source in self.dependency_sources:
            if not isinstance(
                source,
                RetailContextDependencySource,
            ):
                raise TypeError(
                    "every dependency source must be a "
                    "RetailContextDependencySource"
                )

            source_key = (
                source.source_type,
                source.source_id,
            )

            if source_key in seen_typed_sources:
                raise ValueError(
                    "duplicate dependency source: "
                    f"{source.source_type.value}:"
                    f"{source.source_id}"
                )

            seen_typed_sources.add(
                source_key
            )

            if (
                source.source_type
                is DependencySourceType.RULE
            ):
                if source.source_id == self.rule_id:
                    raise ValueError(
                        "derived rule cannot depend on itself: "
                        f"{self.rule_id}"
                    )

                if source.source_id in seen_ids:
                    raise ValueError(
                        "duplicate source rule_id: "
                        f"{source.source_id}"
                    )

                seen_ids.add(
                    source.source_id
                )
