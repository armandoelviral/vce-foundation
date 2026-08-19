import importlib.util
import json
from pathlib import Path

import pytest

from sp001.services.retail_context_assessment_report_consistency import (
    validate_retail_context_assessment_report_consistency,
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
        "rcp001_retail_report_for_consistency_validation",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "canonical retail report fixtures unavailable"
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


def modify_payload(
    modifier,
) -> str:
    document = json.loads(
        create_payload(),
    )

    modifier(
        document,
    )

    return json.dumps(
        document,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
        allow_nan=False,
    )


def test_canonical_report_passes_consistency_validation() -> None:
    assert (
        validate_retail_context_assessment_report_consistency(
            payload=create_payload(),
        )
        is True
    )


def test_empty_json_is_rejected_before_consistency_checks() -> None:
    with pytest.raises(
        ValueError,
        match="missing required report fields",
    ):
        validate_retail_context_assessment_report_consistency(
            payload="{}",
        )


def test_non_string_payload_is_rejected() -> None:
    with pytest.raises(
        TypeError,
        match="payload must be a string",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=None,
        )


def test_total_rules_must_match_actual_rule_count() -> None:
    payload = modify_payload(
        lambda document: document.update(
            {
                "total_rules": 999,
            }
        )
    )

    with pytest.raises(
        ValueError,
        match="total_rules must match actual rule count",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_empty_rule_collection_is_rejected() -> None:
    def remove_rules(document):
        document["rules"] = []
        document["total_rules"] = 0

    payload = modify_payload(
        remove_rules,
    )

    with pytest.raises(
        ValueError,
        match="rules must not be empty",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_duplicate_rule_identity_is_rejected() -> None:
    def duplicate_identity(document):
        document["rules"][1][
            "rule_id"
        ] = document["rules"][0][
            "rule_id"
        ]

    payload = modify_payload(
        duplicate_identity,
    )

    with pytest.raises(
        ValueError,
        match="duplicate rule_id",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "directly_observed_count",
        "derived_count",
        "evidence_assessed_count",
    ),
)
def test_provenance_count_must_match_rule_records(
    field: str,
) -> None:
    def alter_count(document):
        document[field] += 1

    payload = modify_payload(
        alter_count,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must match rule provenance",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_provenance_distribution_cannot_be_rebalanced_falsely() -> None:
    def rebalance_counts(document):
        document["directly_observed_count"] -= 1
        document["derived_count"] += 1

    payload = modify_payload(
        rebalance_counts,
    )

    with pytest.raises(
        ValueError,
        match="directly_observed_count must match rule provenance",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "total_improved_count",
        "unchanged_count",
        "regressed_count",
        "indeterminate_count",
    ),
)
def test_change_count_must_match_rule_records(
    field: str,
) -> None:
    def alter_count(document):
        document[field] += 1

    payload = modify_payload(
        alter_count,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must match rule changes",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_change_distribution_cannot_be_rebalanced_falsely() -> None:
    def rebalance_counts(document):
        document["unchanged_count"] -= 1
        document["regressed_count"] += 1

    payload = modify_payload(
        rebalance_counts,
    )

    with pytest.raises(
        ValueError,
        match="unchanged_count must match rule changes",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "directly_observed_improved_count",
        "derived_improved_count",
    ),
)
def test_improvement_provenance_count_must_match_rule_records(
    field: str,
) -> None:
    def alter_count(document):
        document[field] += 1

    payload = modify_payload(
        alter_count,
    )

    with pytest.raises(
        ValueError,
        match=f"{field} must match improved rule provenance",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_improvement_distribution_cannot_be_rebalanced_falsely() -> None:
    def rebalance_counts(document):
        document["directly_observed_improved_count"] -= 1
        document["derived_improved_count"] += 1

    payload = modify_payload(
        rebalance_counts,
    )

    with pytest.raises(
        ValueError,
        match=(
            "directly_observed_improved_count "
            "must match improved rule provenance"
        ),
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_missing_declared_evidence_identity_is_rejected() -> None:
    def remove_evidence(document):
        document["evidence_ids"].remove(
            "ART-002",
        )

    payload = modify_payload(
        remove_evidence,
    )

    with pytest.raises(
        ValueError,
        match="evidence_ids must match rule evidence references",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_unreferenced_declared_evidence_identity_is_rejected() -> None:
    def add_evidence(document):
        document["evidence_ids"].append(
            "ART-999",
        )

    payload = modify_payload(
        add_evidence,
    )

    with pytest.raises(
        ValueError,
        match="evidence_ids must match rule evidence references",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_duplicate_declared_evidence_identity_is_rejected() -> None:
    def duplicate_evidence(document):
        document["evidence_ids"].append(
            document["evidence_ids"][0],
        )

    payload = modify_payload(
        duplicate_evidence,
    )

    with pytest.raises(
        ValueError,
        match="duplicate evidence_id",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "initial_evidence_ids",
        "final_evidence_ids",
    ),
)
def test_duplicate_rule_evidence_identity_is_rejected(
    field: str,
) -> None:
    def duplicate_evidence(document):
        for rule in document["rules"]:
            if rule[field]:
                rule[field].append(
                    rule[field][0],
                )
                return

        raise RuntimeError(
            "canonical rule evidence unavailable"
        )

    payload = modify_payload(
        duplicate_evidence,
    )

    with pytest.raises(
        ValueError,
        match="duplicate rule evidence_id",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


@pytest.mark.parametrize(
    "field",
    (
        "initial_evidence_ids",
        "final_evidence_ids",
    ),
)
def test_empty_rule_evidence_identity_is_rejected(
    field: str,
) -> None:
    def append_empty_evidence(document):
        document["rules"][0][field].append(
            "   ",
        )

    payload = modify_payload(
        append_empty_evidence,
    )

    with pytest.raises(
        ValueError,
        match="rule evidence_id must not be empty",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_empty_declared_evidence_identity_is_rejected() -> None:
    def append_empty_evidence(document):
        document["evidence_ids"].append(
            "   ",
        )

    payload = modify_payload(
        append_empty_evidence,
    )

    with pytest.raises(
        ValueError,
        match="evidence_id must not be empty",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_duplicate_context_policy_identity_is_rejected() -> None:
    def duplicate_policy(document):
        document["context_policy_ids"].append(
            document["context_policy_ids"][0],
        )

    payload = modify_payload(
        duplicate_policy,
    )

    with pytest.raises(
        ValueError,
        match="duplicate context_policy_id",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_empty_context_policy_identity_is_rejected() -> None:
    def append_empty_policy(document):
        document["context_policy_ids"].append(
            "   ",
        )

    payload = modify_payload(
        append_empty_policy,
    )

    with pytest.raises(
        ValueError,
        match="context_policy_id must not be empty",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_duplicate_disputed_dimension_identity_is_rejected() -> None:
    def duplicate_dimension(document):
        document["disputed_dimension_ids"].append(
            document["disputed_dimension_ids"][0],
        )

    payload = modify_payload(
        duplicate_dimension,
    )

    with pytest.raises(
        ValueError,
        match="duplicate disputed_dimension_id",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_empty_disputed_dimension_identity_is_rejected() -> None:
    def append_empty_dimension(document):
        document["disputed_dimension_ids"].append(
            "   ",
        )

    payload = modify_payload(
        append_empty_dimension,
    )

    with pytest.raises(
        ValueError,
        match="disputed_dimension_id must not be empty",
    ):
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )


def test_validation_preserves_canonical_case_accounting() -> None:
    payload = create_payload()

    document = json.loads(
        payload,
    )

    assert document["total_rules"] == 35
    assert document["directly_observed_count"] == 23
    assert document["derived_count"] == 7
    assert document["evidence_assessed_count"] == 5
    assert document["total_improved_count"] == 14
    assert document["unchanged_count"] == 16
    assert document["regressed_count"] == 0
    assert document["indeterminate_count"] == 5

    assert (
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )
        is True
    )


def test_consistency_validation_does_not_require_digest() -> None:
    payload = create_payload()

    assert (
        validate_retail_context_assessment_report_consistency(
            payload=payload,
        )
        is True
    )
