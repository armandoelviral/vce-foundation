import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from typing import Callable

import pytest

from sp001.contracts.security_admission_assessment_status import (
    SecurityAdmissionAssessmentStatus,
)
from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_domain_assessment import (
    SecurityAdmissionEvidenceDomainAssessment,
)
from sp001.contracts.security_admission_evidence_domain_assessment_set import (
    SecurityAdmissionEvidenceDomainAssessmentSet,
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
from tests.test_security_admission_evidence_domain_assessment import (
    create_byte_length_not_satisfied_outcome,
    create_media_type_not_satisfied_outcome,
)


Domain = SecurityAdmissionEvidenceDomain
Status = SecurityAdmissionAssessmentStatus
ResolutionOutcome = SecurityAdmissionEvidenceCoverageResolutionOutcome
ResolutionFactory = Callable[[], ResolutionOutcome]


def create_set(
    domains: tuple[SecurityAdmissionEvidenceDomain, ...] = (
        Domain.MEDIA_TYPE,
    ),
    factories: tuple[ResolutionFactory, ...] = (
        create_media_type_conclusive_outcome,
    ),
    statuses: tuple[SecurityAdmissionAssessmentStatus, ...] = (
        Status.SATISFIED,
    ),
) -> SecurityAdmissionEvidenceDomainAssessmentSet:
    outcome_set = create_resolution_set(domains, factories)
    closure = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=outcome_set,
    )
    assessments = tuple(
        SecurityAdmissionEvidenceDomainAssessment(
            coverage_closure=closure,
            domain=domain,
            resolution_outcome=resolution_outcome,
            status=status,
        )
        for domain, resolution_outcome, status in zip(
            domains,
            outcome_set.outcomes,
            statuses,
        )
    )
    return SecurityAdmissionEvidenceDomainAssessmentSet(
        coverage_closure=closure,
        assessments=assessments,
    )


def create_two_domain_set(
) -> SecurityAdmissionEvidenceDomainAssessmentSet:
    return create_set(
        (
            Domain.MEDIA_TYPE,
            Domain.BYTE_LENGTH,
        ),
        (
            create_media_type_conclusive_outcome,
            create_byte_length_indeterminate_outcome,
        ),
        (
            Status.SATISFIED,
            Status.INDETERMINATE,
        ),
    )


def test_fields_are_exact() -> None:
    set_fields = fields(
        SecurityAdmissionEvidenceDomainAssessmentSet
    )
    assert tuple(field.name for field in set_fields) == (
        "coverage_closure",
        "assessments",
    )
    assert (
        set_fields[0].type
        is SecurityAdmissionEvidenceCoverageClosure
    )
    assert set_fields[1].type == tuple[
        SecurityAdmissionEvidenceDomainAssessment,
        ...,
    ]


def test_assessment_set_is_immutable_and_slotted() -> None:
    assessment_set = create_set()
    assert not hasattr(assessment_set, "__dict__")
    with pytest.raises(FrozenInstanceError):
        assessment_set.assessments = ()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    assessment_set = create_set()
    closure = assessment_set.coverage_closure
    assessments = assessment_set.assessments

    reconstructed = SecurityAdmissionEvidenceDomainAssessmentSet(
        coverage_closure=closure,
        assessments=assessments,
    )

    assert reconstructed.coverage_closure is closure
    assert reconstructed.assessments is assessments


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
def test_each_canonical_assessment_variant_is_preserved(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
    status: SecurityAdmissionAssessmentStatus,
) -> None:
    assessment_set = create_set(
        (domain,),
        (factory,),
        (status,),
    )
    assessment = assessment_set.assessments[0]

    assert assessment.domain is domain
    assert assessment.status is status
    assert (
        assessment.coverage_closure
        is assessment_set.coverage_closure
    )


@pytest.mark.parametrize(
    ("domains", "factories", "statuses"),
    (
        (
            (
                Domain.MEDIA_TYPE,
                Domain.BYTE_LENGTH,
            ),
            (
                create_media_type_conclusive_outcome,
                create_byte_length_indeterminate_outcome,
            ),
            (
                Status.SATISFIED,
                Status.INDETERMINATE,
            ),
        ),
        (
            (
                Domain.BYTE_LENGTH,
                Domain.MEDIA_TYPE,
            ),
            (
                create_byte_length_not_satisfied_outcome,
                create_media_type_indeterminate_outcome,
            ),
            (
                Status.NOT_SATISFIED,
                Status.INDETERMINATE,
            ),
        ),
    ),
)
def test_assessments_preserve_policy_order_and_outcome_correspondence(
    domains: tuple[SecurityAdmissionEvidenceDomain, ...],
    factories: tuple[ResolutionFactory, ...],
    statuses: tuple[SecurityAdmissionAssessmentStatus, ...],
) -> None:
    assessment_set = create_set(
        domains,
        factories,
        statuses,
    )
    outcomes = (
        assessment_set.coverage_closure
        .resolution_outcome_set
        .outcomes
    )

    assert tuple(
        assessment.domain
        for assessment in assessment_set.assessments
    ) == domains
    assert all(
        assessment.resolution_outcome is outcome
        for assessment, outcome in zip(
            assessment_set.assessments,
            outcomes,
        )
    )


def test_complete_policy_lineage_remains_reachable() -> None:
    assessment_set = create_two_domain_set()
    coverage_identity = (
        assessment_set.coverage_closure
        .resolution_outcome_set
        .coverage_identity
    )
    requirements = (
        coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
    )

    assert requirements.required_evidence_domains == (
        Domain.MEDIA_TYPE,
        Domain.BYTE_LENGTH,
    )
    assert all(
        assessment.resolution_outcome.coverage_identity
        is coverage_identity
        for assessment in assessment_set.assessments
    )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_closure_requires_nominal_type(
    invalid_value: object,
) -> None:
    assessment_set = create_set()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        replace(
            assessment_set,
            coverage_closure=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, [], [object()], object()),
)
def test_assessments_requires_immutable_tuple(
    invalid_value: object,
) -> None:
    assessment_set = create_set()
    with pytest.raises(
        TypeError,
        match="assessments must be an immutable tuple",
    ):
        replace(
            assessment_set,
            assessments=invalid_value,  # type: ignore[arg-type]
        )


def test_assessments_must_not_be_empty() -> None:
    assessment_set = create_set()
    with pytest.raises(
        ValueError,
        match="assessments must not be empty",
    ):
        replace(assessment_set, assessments=())


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_each_assessment_requires_nominal_type(
    invalid_value: object,
) -> None:
    assessment_set = create_set()
    with pytest.raises(
        TypeError,
        match=(
            "assessments must contain "
            "SecurityAdmissionEvidenceDomainAssessment values"
        ),
    ):
        replace(
            assessment_set,
            assessments=(invalid_value,),  # type: ignore[arg-type]
        )


def test_missing_required_domain_assessment_is_rejected() -> None:
    assessment_set = create_two_domain_set()
    with pytest.raises(
        ValueError,
        match=(
            "assessments must contain exactly one assessment "
            "for every required evidence domain"
        ),
    ):
        replace(
            assessment_set,
            assessments=(assessment_set.assessments[0],),
        )


def test_additional_assessment_is_rejected() -> None:
    assessment_set = create_set()
    assessment = assessment_set.assessments[0]
    with pytest.raises(
        ValueError,
        match=(
            "assessments must contain exactly one assessment "
            "for every required evidence domain"
        ),
    ):
        replace(
            assessment_set,
            assessments=(assessment, assessment),
        )


def test_duplicate_assessment_cannot_replace_required_domain() -> None:
    assessment_set = create_two_domain_set()
    media_assessment = assessment_set.assessments[0]
    with pytest.raises(
        ValueError,
        match=(
            "assessments must preserve required evidence domain order"
        ),
    ):
        replace(
            assessment_set,
            assessments=(
                media_assessment,
                media_assessment,
            ),
        )


def test_assessments_must_preserve_policy_order() -> None:
    assessment_set = create_two_domain_set()
    with pytest.raises(
        ValueError,
        match=(
            "assessments must preserve required evidence domain order"
        ),
    ):
        replace(
            assessment_set,
            assessments=tuple(
                reversed(assessment_set.assessments)
            ),
        )


def test_equal_but_different_closure_occurrence_is_rejected() -> None:
    assessment_set = create_set()
    different_closure = replace(
        assessment_set.coverage_closure
    )
    assert different_closure == assessment_set.coverage_closure
    assert different_closure is not assessment_set.coverage_closure

    with pytest.raises(
        ValueError,
        match=(
            "each assessment must use the exact coverage closure"
        ),
    ):
        replace(
            assessment_set,
            coverage_closure=different_closure,
        )


def test_assessments_from_foreign_closure_are_rejected() -> None:
    assessment_set = create_set()
    foreign_set = create_set()

    with pytest.raises(
        ValueError,
        match=(
            "each assessment must use the exact coverage closure"
        ),
    ):
        replace(
            assessment_set,
            assessments=foreign_set.assessments,
        )


def test_blockage_cannot_enter_assessment_set() -> None:
    assessment_set = create_set()
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)

    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        replace(
            assessment_set,
            coverage_closure=blockage,  # type: ignore[arg-type]
        )


def test_decision_classification_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceDomainAssessmentSet
        )
    }
    assert names.isdisjoint(
        {
            "admission_decision",
            "rejection",
            "classification",
            "authority",
            "authorized_by",
        }
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceDomainAssessmentSet
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceDomainAssessmentSet
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
