import ast
import inspect

from dataclasses import fields
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
from sp001.contracts.security_admission_evidence_domain_assessment_set import (
    SecurityAdmissionEvidenceDomainAssessmentSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_domain_assessment_set_projection import (
    project_security_admission_evidence_domain_assessment_set,
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


def create_closure(
    domains: tuple[SecurityAdmissionEvidenceDomain, ...] = (
        Domain.MEDIA_TYPE,
    ),
    factories: tuple[ResolutionFactory, ...] = (
        create_media_type_conclusive_outcome,
    ),
) -> SecurityAdmissionEvidenceCoverageClosure:
    return SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=create_resolution_set(
            domains,
            factories,
        ),
    )


def test_projection_returns_canonical_assessment_set() -> None:
    result = (
        project_security_admission_evidence_domain_assessment_set(
            create_closure()
        )
    )
    assert isinstance(
        result,
        SecurityAdmissionEvidenceDomainAssessmentSet,
    )


def test_projection_preserves_exact_closure_reference() -> None:
    closure = create_closure()
    result = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )
    assert result.coverage_closure is closure
    assert all(
        assessment.coverage_closure is closure
        for assessment in result.assessments
    )


def test_projection_preserves_exact_outcome_references() -> None:
    closure = create_closure(
        (
            Domain.MEDIA_TYPE,
            Domain.BYTE_LENGTH,
        ),
        (
            create_media_type_conclusive_outcome,
            create_byte_length_indeterminate_outcome,
        ),
    )
    result = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )
    assert all(
        assessment.resolution_outcome is resolution_outcome
        for assessment, resolution_outcome in zip(
            result.assessments,
            closure.resolution_outcome_set.outcomes,
        )
    )


@pytest.mark.parametrize(
    ("domain", "factory", "expected_status"),
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
def test_each_resolved_outcome_projects_exact_canonical_status(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
    expected_status: SecurityAdmissionAssessmentStatus,
) -> None:
    closure = create_closure(
        (domain,),
        (factory,),
    )
    result = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )
    assessment = result.assessments[0]

    assert assessment.domain is domain
    assert assessment.status is expected_status


@pytest.mark.parametrize(
    ("domains", "factories", "expected_statuses"),
    (
        (
            (
                Domain.MEDIA_TYPE,
                Domain.BYTE_LENGTH,
            ),
            (
                create_media_type_not_satisfied_outcome,
                create_byte_length_indeterminate_outcome,
            ),
            (
                Status.NOT_SATISFIED,
                Status.INDETERMINATE,
            ),
        ),
        (
            (
                Domain.BYTE_LENGTH,
                Domain.MEDIA_TYPE,
            ),
            (
                create_byte_length_conclusive_outcome,
                create_media_type_indeterminate_outcome,
            ),
            (
                Status.SATISFIED,
                Status.INDETERMINATE,
            ),
        ),
    ),
)
def test_projection_preserves_policy_order(
    domains: tuple[SecurityAdmissionEvidenceDomain, ...],
    factories: tuple[ResolutionFactory, ...],
    expected_statuses: tuple[
        SecurityAdmissionAssessmentStatus,
        ...,
    ],
) -> None:
    result = (
        project_security_admission_evidence_domain_assessment_set(
            create_closure(domains, factories)
        )
    )

    assert tuple(
        assessment.domain
        for assessment in result.assessments
    ) == domains
    assert tuple(
        assessment.status
        for assessment in result.assessments
    ) == expected_statuses


def test_projection_is_exhaustive() -> None:
    closure = create_closure(
        (
            Domain.MEDIA_TYPE,
            Domain.BYTE_LENGTH,
        ),
        (
            create_media_type_conclusive_outcome,
            create_byte_length_conclusive_outcome,
        ),
    )
    result = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )

    assert len(result.assessments) == len(
        closure.resolution_outcome_set.outcomes
    )
    assert len(result.assessments) == 2


def test_repeated_projection_is_deterministic() -> None:
    closure = create_closure(
        (
            Domain.MEDIA_TYPE,
            Domain.BYTE_LENGTH,
        ),
        (
            create_media_type_not_satisfied_outcome,
            create_byte_length_indeterminate_outcome,
        ),
    )

    first = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )
    second = (
        project_security_admission_evidence_domain_assessment_set(
            closure
        )
    )

    assert first == second
    assert first is not second
    assert first.assessments is not second.assessments
    assert all(
        left.resolution_outcome is right.resolution_outcome
        for left, right in zip(
            first.assessments,
            second.assessments,
        )
    )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_projection_requires_complete_closure(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        project_security_admission_evidence_domain_assessment_set(
            invalid_value  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "domain",
    (
        Domain.MEDIA_TYPE,
        Domain.BYTE_LENGTH,
    ),
)
def test_blockage_cannot_enter_projection(
    domain: SecurityAdmissionEvidenceDomain,
) -> None:
    blockage = create_first_domain_blockage(domain)
    with pytest.raises(
        TypeError,
        match=(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        ),
    ):
        project_security_admission_evidence_domain_assessment_set(
            blockage  # type: ignore[arg-type]
        )


def test_projection_introduces_no_decision_or_authority_fields() -> None:
    result = (
        project_security_admission_evidence_domain_assessment_set(
            create_closure()
        )
    )
    names = {
        field.name
        for field in fields(type(result))
    }
    names.update(
        field.name
        for assessment in result.assessments
        for field in fields(type(assessment))
    )

    assert names.isdisjoint(
        {
            "admission_decision",
            "rejection",
            "classification",
            "authority",
            "authorized_by",
        }
    )


def test_projection_executes_no_resolver_or_external_capability() -> None:
    module = inspect.getmodule(
        project_security_admission_evidence_domain_assessment_set
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }

    assert called_names.isdisjoint(
        {
            "media_type_resolver",
            "byte_length_resolver",
            "open",
            "print",
            "input",
        }
    )


def test_service_defines_projection_only() -> None:
    module = inspect.getmodule(
        project_security_admission_evidence_domain_assessment_set
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {
        "project_security_admission_evidence_domain_assessment_set",
        "_media_type_status",
        "_byte_length_status",
    }


def test_service_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        project_security_admission_evidence_domain_assessment_set
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    }

    assert roots == {"sp001"}
