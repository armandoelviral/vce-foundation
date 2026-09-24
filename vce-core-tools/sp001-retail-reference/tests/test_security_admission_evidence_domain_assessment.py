import ast
import inspect
from collections.abc import Callable
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_assessment_status import (
    SecurityAdmissionAssessmentStatus,
)
from sp001.contracts.security_admission_candidate_byte_length_comparison_result import (
    SecurityAdmissionByteLengthComparisonStatus,
)
from sp001.contracts.security_admission_candidate_media_type_comparison_result import (
    SecurityAdmissionMediaTypeComparisonStatus,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_domain_assessment import (
    SecurityAdmissionEvidenceDomainAssessment,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_closure import (
    create_resolution_set,
)
from tests.test_security_admission_evidence_coverage_closure_blockage import (
    create_first_domain_blockage,
)
from tests.test_security_admission_evidence_coverage_resolution_outcome_set import (
    create_byte_length_conclusive_outcome,
    create_byte_length_indeterminate_outcome,
    create_media_type_conclusive_outcome,
    create_media_type_indeterminate_outcome,
)


Domain = SecurityAdmissionEvidenceDomain
Status = SecurityAdmissionAssessmentStatus
ResolutionOutcome = SecurityAdmissionEvidenceCoverageResolutionOutcome
ResolutionFactory = Callable[[], ResolutionOutcome]


def create_media_type_not_satisfied_outcome(
) -> SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome:
    outcome = create_media_type_conclusive_outcome()
    assert isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
    )
    value = outcome.outcome
    governed = (
        value
        .evaluation_record_media_type_observation_selection_comparison_result_binding
    )
    recorded = (
        governed.evaluation_record_media_type_comparison_result_binding
    )
    result_binding = recorded.media_type_comparison_result_binding
    result = replace(
        result_binding.media_type_comparison_result,
        match_status=(
            SecurityAdmissionMediaTypeComparisonStatus.DOES_NOT_MATCH
        ),
    )
    changed_result_binding = replace(
        result_binding,
        media_type_comparison_result=result,
    )
    changed_recorded = replace(
        recorded,
        media_type_comparison_result_binding=changed_result_binding,
    )
    selection_binding = (
        governed.observation_selection_comparison_result_binding
    )
    changed_selection_binding = replace(
        selection_binding,
        media_type_comparison_result_binding=changed_result_binding,
    )
    changed_governed = replace(
        governed,
        observation_selection_comparison_result_binding=(
            changed_selection_binding
        ),
        evaluation_record_media_type_comparison_result_binding=(
            changed_recorded
        ),
    )
    coverage_binding = (
        value.evidence_coverage_media_type_comparison_result_binding
    )
    changed_coverage_binding = replace(
        coverage_binding,
        evaluation_record_media_type_comparison_result_binding=(
            changed_recorded
        ),
    )
    changed_value = replace(
        value,
        evaluation_record_media_type_observation_selection_comparison_result_binding=(
            changed_governed
        ),
        evidence_coverage_media_type_comparison_result_binding=(
            changed_coverage_binding
        ),
    )
    return replace(outcome, outcome=changed_value)


def create_byte_length_not_satisfied_outcome(
) -> SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome:
    outcome = create_byte_length_conclusive_outcome()
    assert isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
    )
    value = outcome.outcome
    governed = (
        value
        .evaluation_record_byte_length_observation_selection_comparison_result_binding
    )
    recorded = (
        governed.evaluation_record_byte_length_comparison_result_binding
    )
    result_binding = recorded.byte_length_comparison_result_binding
    result = replace(
        result_binding.byte_length_comparison_result,
        match_status=(
            SecurityAdmissionByteLengthComparisonStatus.DOES_NOT_MATCH
        ),
    )
    changed_result_binding = replace(
        result_binding,
        byte_length_comparison_result=result,
    )
    changed_recorded = replace(
        recorded,
        byte_length_comparison_result_binding=changed_result_binding,
    )
    selection_binding = (
        governed.observation_selection_comparison_result_binding
    )
    changed_selection_binding = replace(
        selection_binding,
        byte_length_comparison_result_binding=changed_result_binding,
    )
    changed_governed = replace(
        governed,
        observation_selection_comparison_result_binding=(
            changed_selection_binding
        ),
        evaluation_record_byte_length_comparison_result_binding=(
            changed_recorded
        ),
    )
    coverage_binding = (
        value.evidence_coverage_byte_length_comparison_result_binding
    )
    changed_coverage_binding = replace(
        coverage_binding,
        evaluation_record_byte_length_comparison_result_binding=(
            changed_recorded
        ),
    )
    changed_value = replace(
        value,
        evaluation_record_byte_length_observation_selection_comparison_result_binding=(
            changed_governed
        ),
        evidence_coverage_byte_length_comparison_result_binding=(
            changed_coverage_binding
        ),
    )
    return replace(outcome, outcome=changed_value)


def create_closure(
    domain: SecurityAdmissionEvidenceDomain = Domain.MEDIA_TYPE,
    factory: ResolutionFactory = create_media_type_conclusive_outcome,
) -> SecurityAdmissionEvidenceCoverageClosure:
    outcome_set = create_resolution_set(
        (domain,),
        (factory,),
    )
    return SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=outcome_set,
    )


def create_assessment(
    domain: SecurityAdmissionEvidenceDomain = Domain.MEDIA_TYPE,
    factory: ResolutionFactory = create_media_type_conclusive_outcome,
    status: SecurityAdmissionAssessmentStatus = Status.SATISFIED,
) -> SecurityAdmissionEvidenceDomainAssessment:
    closure = create_closure(domain, factory)
    outcome = closure.resolution_outcome_set.outcomes[0]
    return SecurityAdmissionEvidenceDomainAssessment(
        coverage_closure=closure,
        domain=domain,
        resolution_outcome=outcome,
        status=status,
    )


def test_fields_are_exact() -> None:
    assessment_fields = fields(
        SecurityAdmissionEvidenceDomainAssessment
    )
    assert tuple(field.name for field in assessment_fields) == (
        "coverage_closure",
        "domain",
        "resolution_outcome",
        "status",
    )
    assert (
        assessment_fields[0].type
        is SecurityAdmissionEvidenceCoverageClosure
    )
    assert assessment_fields[1].type is SecurityAdmissionEvidenceDomain
    assert (
        assessment_fields[2].type
        == SecurityAdmissionEvidenceCoverageResolutionOutcome
    )
    assert assessment_fields[3].type is SecurityAdmissionAssessmentStatus


def test_assessment_is_immutable_and_slotted() -> None:
    assessment = create_assessment()
    assert not hasattr(assessment, "__dict__")
    with pytest.raises(FrozenInstanceError):
        assessment.status = Status.INDETERMINATE  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    assessment = create_assessment()
    closure = assessment.coverage_closure
    outcome = assessment.resolution_outcome
    reconstructed = SecurityAdmissionEvidenceDomainAssessment(
        coverage_closure=closure,
        domain=assessment.domain,
        resolution_outcome=outcome,
        status=assessment.status,
    )
    assert reconstructed.coverage_closure is closure
    assert reconstructed.resolution_outcome is outcome


@pytest.mark.parametrize(
    ("domain", "factory", "status"),
    (
        (
            Domain.MEDIA_TYPE,
            create_media_type_conclusive_outcome,
            Status.SATISFIED,
        ),
        (
            Domain.MEDIA_TYPE,
            create_media_type_not_satisfied_outcome,
            Status.NOT_SATISFIED,
        ),
        (
            Domain.MEDIA_TYPE,
            create_media_type_indeterminate_outcome,
            Status.INDETERMINATE,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_conclusive_outcome,
            Status.SATISFIED,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_not_satisfied_outcome,
            Status.NOT_SATISFIED,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_indeterminate_outcome,
            Status.INDETERMINATE,
        ),
    ),
)
def test_each_resolved_outcome_maps_to_exact_canonical_status(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
    status: SecurityAdmissionAssessmentStatus,
) -> None:
    assessment = create_assessment(domain, factory, status)
    assert assessment.domain is domain
    assert assessment.status is status


@pytest.mark.parametrize(
    ("domain", "factory", "wrong_status"),
    (
        (
            Domain.MEDIA_TYPE,
            create_media_type_conclusive_outcome,
            Status.NOT_SATISFIED,
        ),
        (
            Domain.MEDIA_TYPE,
            create_media_type_not_satisfied_outcome,
            Status.SATISFIED,
        ),
        (
            Domain.MEDIA_TYPE,
            create_media_type_indeterminate_outcome,
            Status.SATISFIED,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_conclusive_outcome,
            Status.INDETERMINATE,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_not_satisfied_outcome,
            Status.INDETERMINATE,
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_indeterminate_outcome,
            Status.NOT_SATISFIED,
        ),
    ),
)
def test_contradictory_status_is_rejected(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
    wrong_status: SecurityAdmissionAssessmentStatus,
) -> None:
    closure = create_closure(domain, factory)
    with pytest.raises(
        ValueError,
        match="status must match the resolved domain outcome",
    ):
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=closure,
            domain=domain,
            resolution_outcome=(
                closure.resolution_outcome_set.outcomes[0]
            ),
            status=wrong_status,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_closure_requires_nominal_type(
    invalid_value: object,
) -> None:
    assessment = create_assessment()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        replace(
            assessment,
            coverage_closure=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, "MEDIA_TYPE"))
def test_domain_requires_nominal_type(invalid_value: object) -> None:
    assessment = create_assessment()
    with pytest.raises(
        TypeError,
        match="domain must be a SecurityAdmissionEvidenceDomain",
    ):
        replace(
            assessment,
            domain=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_resolution_outcome_requires_nominal_type(
    invalid_value: object,
) -> None:
    assessment = create_assessment()
    with pytest.raises(
        TypeError,
        match=(
            "resolution_outcome must be a "
            "SecurityAdmissionEvidenceCoverageResolutionOutcome"
        ),
    ):
        replace(
            assessment,
            resolution_outcome=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, 1, True, "SATISFIED"),
)
def test_status_requires_nominal_type(invalid_value: object) -> None:
    assessment = create_assessment()
    with pytest.raises(
        TypeError,
        match="status must be a SecurityAdmissionAssessmentStatus",
    ):
        replace(
            assessment,
            status=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("domain", "factory", "wrong_domain", "message"),
    (
        (
            Domain.MEDIA_TYPE,
            create_media_type_conclusive_outcome,
            Domain.BYTE_LENGTH,
            "media-type resolution_outcome requires BYTE_LENGTH domain",
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_conclusive_outcome,
            Domain.MEDIA_TYPE,
            "byte-length resolution_outcome requires MEDIA_TYPE domain",
        ),
    ),
)
def test_resolution_outcome_requires_matching_domain(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
    wrong_domain: SecurityAdmissionEvidenceDomain,
    message: str,
) -> None:
    closure = create_closure(domain, factory)
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=closure,
            domain=wrong_domain,
            resolution_outcome=(
                closure.resolution_outcome_set.outcomes[0]
            ),
            status=Status.SATISFIED,
        )


def test_resolution_outcome_must_be_exact_retained_occurrence() -> None:
    closure = create_closure()
    retained = closure.resolution_outcome_set.outcomes[0]
    equal_but_distinct = replace(retained)
    assert equal_but_distinct == retained
    assert equal_but_distinct is not retained
    with pytest.raises(
        ValueError,
        match="resolution_outcome must be retained by coverage_closure",
    ):
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=closure,
            domain=Domain.MEDIA_TYPE,
            resolution_outcome=equal_but_distinct,
            status=Status.SATISFIED,
        )


def test_outcome_from_another_closure_is_rejected() -> None:
    closure = create_closure()
    foreign_closure = create_closure()
    with pytest.raises(
        ValueError,
        match="resolution_outcome must be retained by coverage_closure",
    ):
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=closure,
            domain=Domain.MEDIA_TYPE,
            resolution_outcome=(
                foreign_closure.resolution_outcome_set.outcomes[0]
            ),
            status=Status.SATISFIED,
        )


def test_closure_blockage_cannot_enter_assessment() -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    closure = create_closure()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=blockage,  # type: ignore[arg-type]
            domain=Domain.MEDIA_TYPE,
            resolution_outcome=(
                closure.resolution_outcome_set.outcomes[0]
            ),
            status=Status.SATISFIED,
        )


def test_assessment_contains_no_decision_or_authority_fields() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvidenceDomainAssessment)
    }
    assert names.isdisjoint(
        {
            "admission_decision",
            "admission_status",
            "classification",
            "rejection",
            "authority",
            "authorized_by",
        }
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceDomainAssessment
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {
        "__post_init__",
        "_media_type_status",
        "_byte_length_status",
    }


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceDomainAssessment
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
