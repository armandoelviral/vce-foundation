from dataclasses import fields
import json

from sp001.contracts.retail_context_rule_observation import (
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
    RetailContextAssessmentRuleReport,
)


REPORT_FIELDS = frozenset(
    field.name
    for field in fields(
        RetailContextAssessmentReport
    )
)

RULE_FIELDS = frozenset(
    field.name
    for field in fields(
        RetailContextAssessmentRuleReport
    )
)

COUNT_FIELDS = (
    "total_rules",
    "directly_observed_count",
    "derived_count",
    "evidence_assessed_count",
    "total_improved_count",
    "directly_observed_improved_count",
    "derived_improved_count",
    "unchanged_count",
    "regressed_count",
    "indeterminate_count",
)

REPORT_REFERENCE_FIELDS = (
    "evidence_ids",
    "disputed_dimension_ids",
    "context_policy_ids",
)

RULE_REFERENCE_FIELDS = (
    "initial_evidence_ids",
    "final_evidence_ids",
)

CLAIM_FIELDS = (
    "customer_acceptance_status",
    "commercial_impact_status",
    "independent_intervention_status",
)


def validate_retail_context_assessment_report_payload(
    *,
    payload: str,
) -> bool:
    """Validate report structure without asserting integrity or authenticity."""

    if not isinstance(
        payload,
        str,
    ):
        raise TypeError(
            "payload must be a string"
        )

    if not payload.strip():
        raise ValueError(
            "payload must not be empty"
        )

    try:
        document = json.loads(
            payload,
        )
    except (
        json.JSONDecodeError,
        UnicodeDecodeError,
    ) as error:
        raise ValueError(
            "payload must contain valid JSON"
        ) from error

    if not isinstance(
        document,
        dict,
    ):
        raise ValueError(
            "report payload must be a JSON object"
        )

    present_fields = frozenset(
        document
    )

    missing_fields = (
        REPORT_FIELDS
        - present_fields
    )

    if missing_fields:
        raise ValueError(
            "missing required report fields: "
            + ", ".join(
                sorted(
                    missing_fields
                )
            )
        )

    unexpected_fields = (
        present_fields
        - REPORT_FIELDS
    )

    if unexpected_fields:
        raise ValueError(
            "unexpected report fields: "
            + ", ".join(
                sorted(
                    unexpected_fields
                )
            )
        )

    for field in (
        "case_id",
        "snapshot_id",
    ):
        identity = document[field]

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

    snapshot_version = document[
        "snapshot_version"
    ]

    if (
        isinstance(
            snapshot_version,
            bool,
        )
        or not isinstance(
            snapshot_version,
            int,
        )
        or snapshot_version < 1
    ):
        raise ValueError(
            "snapshot_version must be a positive integer"
        )

    for field in COUNT_FIELDS:
        count = document[field]

        if (
            isinstance(
                count,
                bool,
            )
            or not isinstance(
                count,
                int,
            )
            or count < 0
        ):
            raise ValueError(
                f"{field} must be a non-negative integer"
            )

    for field in REPORT_REFERENCE_FIELDS:
        if not isinstance(
            document[field],
            list,
        ):
            raise ValueError(
                f"{field} must be a JSON array"
            )

    for field in CLAIM_FIELDS:
        if document[field] != "NOT_ESTABLISHED":
            raise ValueError(
                f"{field} must remain NOT_ESTABLISHED"
            )

    rules = document[
        "rules"
    ]

    if not isinstance(
        rules,
        list,
    ):
        raise ValueError(
            "rules must be a JSON array"
        )

    observation_statuses = frozenset(
        status.value
        for status in RuleObservationStatus
    )

    change_statuses = frozenset(
        status.value
        for status in ObservationChangeStatus
    )

    provenance_types = frozenset(
        classification.value
        for classification in RuleProvenanceType
    )

    for rule in rules:
        if not isinstance(
            rule,
            dict,
        ):
            raise ValueError(
                "rule record must be a JSON object"
            )

        present_rule_fields = frozenset(
            rule
        )

        missing_rule_fields = (
            RULE_FIELDS
            - present_rule_fields
        )

        if missing_rule_fields:
            raise ValueError(
                "missing required rule fields: "
                + ", ".join(
                    sorted(
                        missing_rule_fields
                    )
                )
            )

        unexpected_rule_fields = (
            present_rule_fields
            - RULE_FIELDS
        )

        if unexpected_rule_fields:
            raise ValueError(
                "unexpected rule fields: "
                + ", ".join(
                    sorted(
                        unexpected_rule_fields
                    )
                )
            )

        rule_id = rule[
            "rule_id"
        ]

        if (
            not isinstance(
                rule_id,
                str,
            )
            or not rule_id.strip()
        ):
            raise ValueError(
                "rule_id must not be empty"
            )

        for field in (
            "initial_status",
            "final_status",
        ):
            status = rule[field]

            if (
                not isinstance(
                    status,
                    str,
                )
                or status not in observation_statuses
            ):
                raise ValueError(
                    f"{field} must be a valid "
                    "RuleObservationStatus"
                )

        change_status = rule[
            "change_status"
        ]

        if (
            not isinstance(
                change_status,
                str,
            )
            or change_status not in change_statuses
        ):
            raise ValueError(
                "change_status must be a valid "
                "ObservationChangeStatus"
            )

        provenance_type = rule[
            "provenance_type"
        ]

        if (
            not isinstance(
                provenance_type,
                str,
            )
            or provenance_type not in provenance_types
        ):
            raise ValueError(
                "provenance_type must be a valid "
                "RuleProvenanceType"
            )

        for field in RULE_REFERENCE_FIELDS:
            if not isinstance(
                rule[field],
                list,
            ):
                raise ValueError(
                    f"{field} must be a JSON array"
                )

    return True
