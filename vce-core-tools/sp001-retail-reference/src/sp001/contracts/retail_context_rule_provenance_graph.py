from dataclasses import dataclass

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
)
from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
    RuleProvenanceType,
)


@dataclass(frozen=True, slots=True)
class RuleProvenanceGraph:
    """Immutable, validated graph of observed and derived retail rules."""

    records: tuple[RetailContextRuleProvenance, ...]
    total_rules: int
    directly_observed_count: int
    derived_count: int
    context_policy_ids: tuple[str, ...] = ()


def build_rule_provenance_graph(
    *,
    records: tuple[RetailContextRuleProvenance, ...],
    context_policy_ids: tuple[str, ...] = (),
) -> RuleProvenanceGraph:
    """Validate rule dependencies and declared contextual policy roots."""

    if not isinstance(
        records,
        tuple,
    ):
        raise TypeError(
            "records must be an immutable tuple"
        )

    if not records:
        raise ValueError(
            "records must not be empty"
        )

    if not isinstance(
        context_policy_ids,
        tuple,
    ):
        raise TypeError(
            "context_policy_ids must be "
            "an immutable tuple"
        )

    declared_policy_ids: set[str] = set()

    for policy_id in context_policy_ids:
        if (
            not isinstance(
                policy_id,
                str,
            )
            or not policy_id.strip()
        ):
            raise ValueError(
                "context policy source_id "
                "must not be empty"
            )

        if policy_id in declared_policy_ids:
            raise ValueError(
                "duplicate context policy source_id: "
                f"{policy_id}"
            )

        declared_policy_ids.add(
            policy_id
        )

    records_by_id: dict[
        str,
        RetailContextRuleProvenance,
    ] = {}

    for record in records:
        if not isinstance(
            record,
            RetailContextRuleProvenance,
        ):
            raise TypeError(
                "every record must be a "
                "RetailContextRuleProvenance"
            )

        if record.rule_id in records_by_id:
            raise ValueError(
                "duplicate rule_id: "
                f"{record.rule_id}"
            )

        records_by_id[
            record.rule_id
        ] = record

    for record in records:
        for source_rule_id in record.source_rule_ids:
            if source_rule_id not in records_by_id:
                raise ValueError(
                    "missing source rule_id: "
                    f"{source_rule_id}"
                )

        for source in record.dependency_sources:
            if (
                source.source_type
                is DependencySourceType.RULE
            ):
                if source.source_id not in records_by_id:
                    raise ValueError(
                        "missing source rule_id: "
                        f"{source.source_id}"
                    )

            elif (
                source.source_type
                is DependencySourceType.CONTEXT_POLICY
            ):
                if source.source_id not in declared_policy_ids:
                    raise ValueError(
                        "missing context policy source_id: "
                        f"{source.source_id}"
                    )

    active: set[str] = set()
    completed: set[str] = set()

    def visit(
        rule_id: str,
    ) -> None:
        if rule_id in completed:
            return

        if rule_id in active:
            raise ValueError(
                "cyclic rule dependency detected"
            )

        active.add(
            rule_id
        )

        record = records_by_id[
            rule_id
        ]

        for source_rule_id in record.source_rule_ids:
            visit(
                source_rule_id
            )

        for source in record.dependency_sources:
            if (
                source.source_type
                is DependencySourceType.RULE
            ):
                visit(
                    source.source_id
                )

        active.remove(
            rule_id
        )

        completed.add(
            rule_id
        )

    for record in records:
        visit(
            record.rule_id
        )

    directly_observed_count = sum(
        record.provenance_type
        is RuleProvenanceType.DIRECTLY_OBSERVED
        for record in records
    )

    derived_count = sum(
        record.provenance_type
        is RuleProvenanceType.DERIVED
        for record in records
    )

    return RuleProvenanceGraph(
        records=records,
        total_rules=len(records),
        directly_observed_count=(
            directly_observed_count
        ),
        derived_count=derived_count,
        context_policy_ids=context_policy_ids,
    )
