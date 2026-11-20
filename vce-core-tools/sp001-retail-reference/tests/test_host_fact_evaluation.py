from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.host_fact_evaluation import (
    REQUIRED_FINDING_CODES,
    DeclaredFindingOutcome,
    HostFactEvaluation,
    HostFactFinding,
)


def finding(**overrides):
    values = {
        "check_code": "ASSERTION_STRUCTURE",
        "outcome": DeclaredFindingOutcome.UNKNOWN,
        "evidence_ids": ("EVIDENCE-001",),
    }
    values.update(overrides)
    return HostFactFinding(**values)


def evaluation(**overrides):
    values = {
        "evaluation_record_id": "RECORD-001",
        "assertion_id": "ASSERTION-001",
        "evaluation_id": "EVALUATION-001",
        "evaluator_id": "EVALUATOR-001",
        "evaluated_at": 100,
        "policy_version": "POLICY-001",
        "findings": (finding(),),
    }
    values.update(overrides)
    return HostFactEvaluation(**values)


def test_valid_finding_preserves_values():
    result = finding()
    assert result.check_code == "ASSERTION_STRUCTURE"
    assert result.outcome is DeclaredFindingOutcome.UNKNOWN


def test_valid_evaluation_preserves_values():
    result = evaluation()
    assert result.assertion_id == "ASSERTION-001"
    assert result.evaluated_at == 100


def test_all_finding_codes_are_accepted():
    for code in REQUIRED_FINDING_CODES:
        assert finding(check_code=code).check_code == code


@pytest.mark.parametrize(
    "invalid",
    ("UNKNOWN_CODE", "HOST-P01", ""),
)
def test_unknown_finding_code_is_rejected(invalid):
    with pytest.raises(ValueError):
        finding(check_code=invalid)


@pytest.mark.parametrize(
    "outcome",
    tuple(DeclaredFindingOutcome),
)
def test_all_declared_outcomes_are_accepted(outcome):
    assert finding(outcome=outcome).outcome is outcome


@pytest.mark.parametrize(
    "invalid",
    ("PASS", None, True, 1),
)
def test_untyped_outcome_is_rejected(invalid):
    with pytest.raises(TypeError):
        finding(outcome=invalid)


@pytest.mark.parametrize(
    "invalid",
    (None, [], "EVIDENCE-001"),
)
def test_invalid_evidence_collection_is_rejected(invalid):
    with pytest.raises(TypeError):
        finding(evidence_ids=invalid)


@pytest.mark.parametrize(
    "invalid",
    ("", " ", None, 7),
)
def test_invalid_evidence_id_is_rejected(invalid):
    with pytest.raises(ValueError):
        finding(evidence_ids=(invalid,))


def test_duplicate_evidence_is_rejected():
    with pytest.raises(ValueError):
        finding(evidence_ids=("E1", "E1"))


def test_empty_evidence_is_allowed():
    assert finding(evidence_ids=()).evidence_ids == ()


@pytest.mark.parametrize(
    "field",
    (
        "evaluation_record_id",
        "assertion_id",
        "evaluation_id",
        "evaluator_id",
        "policy_version",
    ),
)
@pytest.mark.parametrize(
    "invalid",
    ("", " ", None, 7),
)
def test_invalid_evaluation_identifier(field, invalid):
    with pytest.raises(ValueError):
        evaluation(**{field: invalid})


@pytest.mark.parametrize(
    "invalid",
    (None, True, False, 1.5, "100"),
)
def test_invalid_evaluated_at_type(invalid):
    with pytest.raises(TypeError):
        evaluation(evaluated_at=invalid)


def test_negative_evaluated_at_is_rejected():
    with pytest.raises(ValueError):
        evaluation(evaluated_at=-1)


def test_future_evaluated_at_is_structurally_allowed():
    assert evaluation(evaluated_at=9999999999).evaluated_at == 9999999999


@pytest.mark.parametrize(
    "invalid",
    (None, [], "finding"),
)
def test_invalid_findings_collection(invalid):
    with pytest.raises(TypeError):
        evaluation(findings=invalid)


def test_empty_findings_are_rejected():
    with pytest.raises(ValueError):
        evaluation(findings=())


def test_invalid_finding_member_is_rejected():
    with pytest.raises(TypeError):
        evaluation(findings=({"check_code": "ASSERTION_STRUCTURE"},))


def test_duplicate_finding_code_is_rejected():
    with pytest.raises(ValueError):
        evaluation(findings=(finding(), finding()))


def test_distinct_findings_are_accepted():
    result = evaluation(
        findings=(
            finding(check_code="ASSERTION_STRUCTURE"),
            finding(check_code="MANDATE_SCOPE"),
        )
    )
    assert len(result.findings) == 2


def test_all_pass_does_not_create_authority():
    result = evaluation(
        findings=(
            finding(
                outcome=DeclaredFindingOutcome.PASS,
                evidence_ids=(),
            ),
        )
    )
    for attribute in (
        "trusted",
        "verified",
        "eligible",
        "accepted",
        "authorized",
    ):
        assert not hasattr(result, attribute)


def test_contradictory_evaluations_remain_distinct():
    passed = evaluation(
        evaluation_record_id="RECORD-PASS",
        findings=(
            finding(outcome=DeclaredFindingOutcome.PASS),
        ),
    )
    failed = evaluation(
        evaluation_record_id="RECORD-FAIL",
        findings=(
            finding(outcome=DeclaredFindingOutcome.FAIL),
        ),
    )

    assert passed.assertion_id == failed.assertion_id
    assert passed != failed


def test_finding_is_immutable():
    result = finding()
    with pytest.raises(FrozenInstanceError):
        result.check_code = "MANDATE_SCOPE"


def test_evaluation_is_immutable():
    result = evaluation()
    with pytest.raises(FrozenInstanceError):
        result.assertion_id = "OTHER"


def test_replace_preserves_validation():
    with pytest.raises(ValueError):
        replace(evaluation(), evaluator_id="")
