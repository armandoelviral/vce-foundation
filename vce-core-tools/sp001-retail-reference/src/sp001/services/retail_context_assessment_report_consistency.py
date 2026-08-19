import json

from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.services.retail_context_assessment_report_payload_validation import (
    validate_retail_context_assessment_report_payload,
)


def validate_retail_context_assessment_report_consistency(
    *,
    payload: str,
) -> bool:
    """Validate report accounting without asserting integrity or authenticity."""

    validate_retail_context_assessment_report_payload(
        payload=payload,
    )

    document = json.loads(
        payload,
    )

    rules = document[
        "rules"
    ]

    if not rules:
        raise ValueError(
            "rules must not be empty"
        )

    if document["total_rules"] != len(
        rules
    ):
        raise ValueError(
            "total_rules must match actual rule count"
        )

    seen_rule_ids: set[str] = set()

    for rule in rules:
        rule_id = rule[
            "rule_id"
        ]

        if rule_id in seen_rule_ids:
            raise ValueError(
                f"duplicate rule_id: {rule_id}"
            )

        seen_rule_ids.add(
            rule_id,
        )

    provenance_fields = (
        (
            "directly_observed_count",
            RuleProvenanceType.DIRECTLY_OBSERVED.value,
        ),
        (
            "derived_count",
            RuleProvenanceType.DERIVED.value,
        ),
        (
            "evidence_assessed_count",
            RuleProvenanceType.EVIDENCE_ASSESSED.value,
        ),
    )

    for field, provenance_type in provenance_fields:
        actual_count = sum(
            1
            for rule in rules
            if (
                rule["provenance_type"]
                == provenance_type
            )
        )

        if document[field] != actual_count:
            raise ValueError(
                f"{field} must match rule provenance"
            )

    change_fields = (
        (
            "total_improved_count",
            ObservationChangeStatus.IMPROVED.value,
        ),
        (
            "unchanged_count",
            ObservationChangeStatus.UNCHANGED.value,
        ),
        (
            "regressed_count",
            ObservationChangeStatus.REGRESSED.value,
        ),
        (
            "indeterminate_count",
            ObservationChangeStatus.INDETERMINATE.value,
        ),
    )

    for field, change_status in change_fields:
        actual_count = sum(
            1
            for rule in rules
            if (
                rule["change_status"]
                == change_status
            )
        )

        if document[field] != actual_count:
            raise ValueError(
                f"{field} must match rule changes"
            )

    improvement_fields = (
        (
            "directly_observed_improved_count",
            RuleProvenanceType.DIRECTLY_OBSERVED.value,
        ),
        (
            "derived_improved_count",
            RuleProvenanceType.DERIVED.value,
        ),
    )

    for field, provenance_type in improvement_fields:
        actual_count = sum(
            1
            for rule in rules
            if (
                rule["change_status"]
                == ObservationChangeStatus.IMPROVED.value
                and rule["provenance_type"]
                == provenance_type
            )
        )

        if document[field] != actual_count:
            raise ValueError(
                f"{field} must match improved rule provenance"
            )

    declared_evidence_ids: set[str] = set()

    for evidence_id in document[
        "evidence_ids"
    ]:
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

        if evidence_id in declared_evidence_ids:
            raise ValueError(
                f"duplicate evidence_id: {evidence_id}"
            )

        declared_evidence_ids.add(
            evidence_id,
        )

    referenced_evidence_ids: set[str] = set()

    for rule in rules:
        for field in (
            "initial_evidence_ids",
            "final_evidence_ids",
        ):
            seen_rule_evidence_ids: set[str] = set()

            for evidence_id in rule[field]:
                if (
                    not isinstance(
                        evidence_id,
                        str,
                    )
                    or not evidence_id.strip()
                ):
                    raise ValueError(
                        "rule evidence_id must not be empty"
                    )

                if evidence_id in seen_rule_evidence_ids:
                    raise ValueError(
                        "duplicate rule evidence_id: "
                        f"{evidence_id}"
                    )

                seen_rule_evidence_ids.add(
                    evidence_id,
                )

                referenced_evidence_ids.add(
                    evidence_id,
                )

    if (
        declared_evidence_ids
        != referenced_evidence_ids
    ):
        raise ValueError(
            "evidence_ids must match rule evidence references"
        )

    identity_collections = (
        (
            "context_policy_ids",
            "context_policy_id",
        ),
        (
            "disputed_dimension_ids",
            "disputed_dimension_id",
        ),
    )

    for field, identity_name in identity_collections:
        seen_identities: set[str] = set()

        for identity in document[field]:
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{identity_name} must not be empty"
                )

            if identity in seen_identities:
                raise ValueError(
                    f"duplicate {identity_name}: "
                    f"{identity}"
                )

            seen_identities.add(
                identity,
            )

    return True
