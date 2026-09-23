import ast
import inspect
from collections.abc import Callable
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
    SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_resolution_outcome_set import (
    create_byte_length_conclusive_outcome,
    create_byte_length_indeterminate_outcome,
    create_coverage_identity,
    create_media_type_conclusive_outcome,
    create_media_type_indeterminate_outcome,
    create_set,
    rebind_outcome,
)


Domain = SecurityAdmissionEvidenceDomain
ResolutionFactory = Callable[
    [],
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
]


def create_resolution_set(
    required_domains: tuple[SecurityAdmissionEvidenceDomain, ...],
    factories: tuple[ResolutionFactory, ...],
) -> SecurityAdmissionEvidenceCoverageResolutionOutcomeSet:
    source_outcomes = tuple(factory() for factory in factories)
    identity = create_coverage_identity(
        required_domains,
        source_outcomes[0].coverage_identity,
    )
    outcomes = tuple(
        rebind_outcome(outcome, identity)
        for outcome in source_outcomes
    )
    return SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
        coverage_identity=identity,
        outcomes=outcomes,
    )


def create_closure() -> SecurityAdmissionEvidenceCoverageClosure:
    return SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=create_set(),
    )


def test_fields_are_exact() -> None:
    closure_fields = fields(SecurityAdmissionEvidenceCoverageClosure)

    assert tuple(field.name for field in closure_fields) == (
        "resolution_outcome_set",
    )
    assert (
        closure_fields[0].type
        is SecurityAdmissionEvidenceCoverageResolutionOutcomeSet
    )


def test_is_immutable() -> None:
    closure = create_closure()

    with pytest.raises(FrozenInstanceError):
        closure.resolution_outcome_set = create_set()  # type: ignore[misc]


def test_uses_slots() -> None:
    closure = create_closure()

    assert hasattr(SecurityAdmissionEvidenceCoverageClosure, "__slots__")
    assert not hasattr(closure, "__dict__")


def test_exact_outcome_set_reference_is_preserved() -> None:
    outcome_set = create_set()

    closure = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=outcome_set,
    )

    assert closure.resolution_outcome_set is outcome_set


def test_complete_coverage_lineage_remains_reachable() -> None:
    closure = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=create_set(
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
        ),
    )

    outcome_set = closure.resolution_outcome_set
    assert (
        outcome_set.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .required_evidence_domains
        == (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
    )
    assert len(outcome_set.outcomes) == 2
    assert all(outcome.outcome is not None for outcome in outcome_set.outcomes)


@pytest.mark.parametrize(
    ("required_domains", "factories"),
    (
        (
            (Domain.MEDIA_TYPE,),
            (create_media_type_conclusive_outcome,),
        ),
        (
            (Domain.MEDIA_TYPE,),
            (create_media_type_indeterminate_outcome,),
        ),
        (
            (Domain.BYTE_LENGTH,),
            (create_byte_length_conclusive_outcome,),
        ),
        (
            (Domain.BYTE_LENGTH,),
            (create_byte_length_indeterminate_outcome,),
        ),
        (
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
            (
                create_media_type_conclusive_outcome,
                create_byte_length_conclusive_outcome,
            ),
        ),
        (
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
            (
                create_media_type_indeterminate_outcome,
                create_byte_length_indeterminate_outcome,
            ),
        ),
        (
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
            (
                create_media_type_conclusive_outcome,
                create_byte_length_indeterminate_outcome,
            ),
        ),
        (
            (Domain.BYTE_LENGTH, Domain.MEDIA_TYPE),
            (
                create_byte_length_indeterminate_outcome,
                create_media_type_conclusive_outcome,
            ),
        ),
    ),
)
def test_conclusive_and_indeterminate_outcomes_close_coverage(
    required_domains: tuple[SecurityAdmissionEvidenceDomain, ...],
    factories: tuple[ResolutionFactory, ...],
) -> None:
    outcome_set = create_resolution_set(
        required_domains,
        factories,
    )

    closure = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=outcome_set,
    )

    assert closure.resolution_outcome_set is outcome_set


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_resolution_outcome_set_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "resolution_outcome_set must be a "
            "SecurityAdmissionEvidenceCoverageResolutionOutcomeSet"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosure(
            resolution_outcome_set=invalid_value,  # type: ignore[arg-type]
        )


def test_reconstructed_equal_closure_has_value_equality() -> None:
    closure = create_closure()

    reconstructed = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=closure.resolution_outcome_set,
    )

    assert reconstructed == closure
    assert reconstructed is not closure


def test_decision_authority_and_status_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionEvidenceCoverageClosure)
    }

    assert names.isdisjoint(
        {
            "coverage_status",
            "admission_status",
            "admission_decision",
            "rejection",
            "authority",
            "authorized",
        }
    )


def test_contract_defines_validation_only() -> None:
    source = inspect.getsource(SecurityAdmissionEvidenceCoverageClosure)
    tree = ast.parse(source)
    methods = [
        node.name
        for node in tree.body[0].body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    ]

    assert methods == ["__post_init__"]


def test_no_external_capability_is_exposed() -> None:
    closure = create_closure()

    for name in (
        "execute",
        "open",
        "send",
        "publish",
        "authorize",
        "admit",
        "reject",
    ):
        assert not hasattr(closure, name)
