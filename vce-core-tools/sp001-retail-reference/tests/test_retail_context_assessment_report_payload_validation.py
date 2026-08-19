import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_payload_validation import (
    validate_retail_context_assessment_report_payload,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)


def load_report_tests():
    path = (
        Path(__file__).resolve().parent
        / "test_retail_context_assessment_report.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_retail_assessment_report_for_payload_validation",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "retail assessment report fixtures unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


REPORT = load_report_tests()


def create_payload() -> str:
    report = REPORT.create_report()

    return serialize_retail_context_assessment_report(
        report=report,
    )


def modify_payload(modifier) -> str:
    document = json.loads(
        create_payload(),
    )

    modifier(
        document,
    )

    return json.dumps(
        document,
        ensure_ascii=False,
    )


def test_valid_canonical_report_payload_passes_validation() -> None:
    assert validate_retail_context_assessment_report_payload(
        payload=create_payload(),
    ) is True


def test_empty_json_object_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="missing required report fields",
    ):
        validate_retail_context_assessment_report_payload(
            payload="{}",
        )


def test_non_string_payload_is_rejected() -> None:
    with pytest.raises(
        TypeError,
        match="payload must be a string",
    ):
        validate_retail_context_assessment_report_payload(
            payload=None,
        )


def test_empty_payload_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="payload must not be empty",
    ):
        validate_retail_context_assessment_report_payload(
            payload="   ",
        )


def test_malformed_json_payload_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="payload must contain valid JSON",
    ):
        validate_retail_context_assessment_report_payload(
            payload="{",
        )


@pytest.mark.parametrize(
    "payload",
    (
        "[]",
        "null",
        "true",
        "1",
        '"report"',
    ),
)
def test_non_object_json_payload_is_rejected(
    payload: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="report payload must be a JSON object",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "case_id",
        "snapshot_id",
        "snapshot_version",
        "rules",
        "total_rules",
        "customer_acceptance_status",
        "commercial_impact_status",
        "independent_intervention_status",
    ),
)
def test_missing_required_report_field_is_rejected(
    field: str,
) -> None:
    payload = modify_payload(
        lambda document: document.pop(
            field,
        )
    )

    with pytest.raises(
        ValueError,
        match="missing required report fields",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_unexpected_report_field_is_rejected() -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "invented_commercial_claim": "VERIFIED",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="unexpected report fields",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "case_id",
        "snapshot_id",
    ),
)
def test_empty_report_identity_is_rejected(
    field: str,
) -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                field: "   ",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "version",
    (
        0,
        -1,
        True,
        "1",
    ),
)
def test_invalid_snapshot_version_is_rejected(
    version,
) -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "snapshot_version": version,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_rules_must_be_json_array() -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "rules": {},
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="rules must be a JSON array",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_rule_record_must_be_json_object() -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "rules": [
                    "CLR-001",
                ],
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="rule record must be a JSON object",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "rule_id",
        "initial_status",
        "final_status",
        "change_status",
        "provenance_type",
        "initial_evidence_ids",
        "final_evidence_ids",
    ),
)
def test_missing_required_rule_field_is_rejected(
    field: str,
) -> None:
    def remove_field(document):
        document["rules"][0].pop(
            field,
        )

    payload = modify_payload(
        remove_field,
    )

    with pytest.raises(
        ValueError,
        match="missing required rule fields",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_unexpected_rule_field_is_rejected() -> None:
    def add_field(document):
        document["rules"][0][
            "invented_authority"
        ] = "VERIFIED"

    payload = modify_payload(
        add_field,
    )

    with pytest.raises(
        ValueError,
        match="unexpected rule fields",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_empty_rule_identity_is_rejected() -> None:
    def clear_identity(document):
        document["rules"][0][
            "rule_id"
        ] = "   "

    payload = modify_payload(
        clear_identity,
    )

    with pytest.raises(
        ValueError,
        match="rule_id must not be empty",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "initial_status",
        "final_status",
    ),
)
def test_unknown_observation_status_is_rejected(
    field: str,
) -> None:
    def replace_status(document):
        document["rules"][0][
            field
        ] = "INVENTED_STATUS"

    payload = modify_payload(
        replace_status,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be a valid RuleObservationStatus",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_unknown_change_status_is_rejected() -> None:
    def replace_status(document):
        document["rules"][0][
            "change_status"
        ] = "INVENTED_CHANGE"

    payload = modify_payload(
        replace_status,
    )

    with pytest.raises(
        ValueError,
        match="change_status must be a valid ObservationChangeStatus",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_unknown_provenance_type_is_rejected() -> None:
    def replace_provenance(document):
        document["rules"][0][
            "provenance_type"
        ] = "INVENTED_PROVENANCE"

    payload = modify_payload(
        replace_provenance,
    )

    with pytest.raises(
        ValueError,
        match="provenance_type must be a valid RuleProvenanceType",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "initial_evidence_ids",
        "final_evidence_ids",
    ),
)
def test_rule_evidence_references_must_be_arrays(
    field: str,
) -> None:
    def replace_references(document):
        document["rules"][0][
            field
        ] = "ART-003"

    payload = modify_payload(
        replace_references,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be a JSON array",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "evidence_ids",
        "disputed_dimension_ids",
        "context_policy_ids",
    ),
)
def test_report_reference_collections_must_be_arrays(
    field: str,
) -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                field: "INVALID",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be a JSON array",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
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
    ),
)
def test_report_counts_must_be_non_negative_integers(
    field: str,
) -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                field: -1,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must be a non-negative integer",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_boolean_report_count_is_rejected() -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "total_rules": True,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="total_rules must be a non-negative integer",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "customer_acceptance_status",
        "commercial_impact_status",
        "independent_intervention_status",
    ),
)
def test_unsupported_commercial_claim_is_rejected(
    field: str,
) -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                field: "VERIFIED",
            }
        )
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must remain NOT_ESTABLISHED",
    ):
        validate_retail_context_assessment_report_payload(
            payload=payload,
        )


def test_validation_does_not_require_digest_or_authenticity() -> None:
    payload = create_payload()

    assert validate_retail_context_assessment_report_payload(
        payload=payload,
    ) is True
