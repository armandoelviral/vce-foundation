import ast
import inspect
from collections.abc import Callable
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
    SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_byte_length_closure_impediment import (
    create_impediment as create_byte_length_impediment,
)
from tests.test_security_admission_evidence_coverage_byte_length_observation_selection_comparison_result_binding import (
    create_binding as create_byte_length_conclusive_binding,
)
from tests.test_security_admission_evidence_coverage_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    create_binding as create_byte_length_indeterminate_binding,
)
from tests.test_security_admission_evidence_coverage_byte_length_resolution_outcome import (
    create_outcome as create_byte_length_outcome,
)
from tests.test_security_admission_evidence_coverage_identity import (
    create_identity,
)
from tests.test_security_admission_evidence_coverage_media_type_closure_impediment import (
    create_impediment as create_media_type_impediment,
)
from tests.test_security_admission_evidence_coverage_media_type_observation_selection_comparison_result_binding import (
    create_binding as create_media_type_conclusive_binding,
)
from tests.test_security_admission_evidence_coverage_media_type_observation_selection_indeterminate_comparison_result_binding import (
    create_binding as create_media_type_indeterminate_binding,
)
from tests.test_security_admission_evidence_coverage_media_type_resolution_outcome import (
    create_outcome as create_media_type_outcome,
)


Domain = SecurityAdmissionEvidenceDomain
ResolutionOutcome = (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
    | SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome
)
ResolutionFactory = Callable[[], ResolutionOutcome]


def create_coverage_identity(
    required_domains: tuple[SecurityAdmissionEvidenceDomain, ...],
    base_identity: SecurityAdmissionEvidenceCoverageIdentity | None = None,
) -> SecurityAdmissionEvidenceCoverageIdentity:
    if base_identity is None:
        base_identity = (
            create_media_type_conclusive_outcome().coverage_identity
        )
    binding = (
        base_identity
        .evaluation_record_policy_evidence_requirements_binding
    )
    requirements = replace(
        binding.policy_evidence_requirements,
        required_evidence_domains=required_domains,
    )
    return replace(
        base_identity,
        evaluation_record_policy_evidence_requirements_binding=replace(
            binding,
            policy_evidence_requirements=requirements,
        ),
    )


def rebind_outcome(
    resolution_outcome: ResolutionOutcome,
    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
) -> ResolutionOutcome:
    value = resolution_outcome.outcome
    nested_coverage_fields = (
        "evidence_coverage_media_type_comparison_result_binding",
        "evidence_coverage_indeterminate_media_type_comparison_result_binding",
        "evidence_coverage_byte_length_comparison_result_binding",
        "evidence_coverage_indeterminate_byte_length_comparison_result_binding",
    )

    for field_name in nested_coverage_fields:
        if hasattr(value, field_name):
            coverage_binding = getattr(value, field_name)
            value = replace(
                value,
                **{
                    field_name: replace(
                        coverage_binding,
                        coverage_identity=coverage_identity,
                    )
                },
            )
            break
    else:
        value = replace(
            value,
            coverage_identity=coverage_identity,
        )

    return replace(
        resolution_outcome,
        coverage_identity=coverage_identity,
        outcome=value,
    )


def create_media_type_conclusive_outcome() -> ResolutionOutcome:
    return create_media_type_outcome(
        create_media_type_conclusive_binding
    )


def create_media_type_indeterminate_outcome() -> ResolutionOutcome:
    return create_media_type_outcome(
        create_media_type_indeterminate_binding
    )


def create_media_type_impediment_outcome() -> ResolutionOutcome:
    return create_media_type_outcome(create_media_type_impediment)


def create_byte_length_conclusive_outcome() -> ResolutionOutcome:
    return create_byte_length_outcome(
        create_byte_length_conclusive_binding
    )


def create_byte_length_indeterminate_outcome() -> ResolutionOutcome:
    return create_byte_length_outcome(
        create_byte_length_indeterminate_binding
    )


def create_byte_length_impediment_outcome() -> ResolutionOutcome:
    return create_byte_length_outcome(create_byte_length_impediment)


def create_set(
    required_domains: tuple[SecurityAdmissionEvidenceDomain, ...] = (
        Domain.MEDIA_TYPE,
    ),
) -> SecurityAdmissionEvidenceCoverageResolutionOutcomeSet:
    factories: dict[
        SecurityAdmissionEvidenceDomain,
        ResolutionFactory,
    ] = {
        Domain.MEDIA_TYPE: create_media_type_conclusive_outcome,
        Domain.BYTE_LENGTH: create_byte_length_conclusive_outcome,
    }
    source_outcomes = tuple(
        factories[domain]()
        for domain in required_domains
    )
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


def test_fields_are_exact() -> None:
    outcome_set_fields = fields(
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet
    )

    assert tuple(field.name for field in outcome_set_fields) == (
        "coverage_identity",
        "outcomes",
    )
    assert (
        outcome_set_fields[0].type
        is SecurityAdmissionEvidenceCoverageIdentity
    )
    assert outcome_set_fields[1].type == tuple[
        SecurityAdmissionEvidenceCoverageResolutionOutcome,
        ...,
    ]


def test_is_immutable() -> None:
    outcome_set = create_set()

    with pytest.raises(FrozenInstanceError):
        outcome_set.outcomes = ()  # type: ignore[misc]


def test_uses_slots() -> None:
    outcome_set = create_set()

    assert hasattr(
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
        "__slots__",
    )
    assert not hasattr(outcome_set, "__dict__")


def test_exact_references_are_preserved() -> None:
    outcome_set = create_set()
    identity = outcome_set.coverage_identity
    outcomes = outcome_set.outcomes

    reconstructed = SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
        coverage_identity=identity,
        outcomes=outcomes,
    )

    assert reconstructed.coverage_identity is identity
    assert reconstructed.outcomes is outcomes


@pytest.mark.parametrize(
    ("domain", "factory"),
    (
        (Domain.MEDIA_TYPE, create_media_type_conclusive_outcome),
        (Domain.MEDIA_TYPE, create_media_type_indeterminate_outcome),
        (Domain.BYTE_LENGTH, create_byte_length_conclusive_outcome),
        (Domain.BYTE_LENGTH, create_byte_length_indeterminate_outcome),
    ),
)
def test_each_resolved_domain_outcome_variant_is_preserved(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
) -> None:
    source_outcome = factory()
    identity = create_coverage_identity(
        (domain,),
        source_outcome.coverage_identity,
    )
    outcome = rebind_outcome(source_outcome, identity)
    outcomes = (outcome,)

    outcome_set = SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
        coverage_identity=identity,
        outcomes=outcomes,
    )

    assert outcome_set.outcomes is outcomes
    assert outcome_set.outcomes[0] is outcome
    assert outcome_set.outcomes[0].outcome is outcome.outcome


@pytest.mark.parametrize(
    ("domain", "factory"),
    (
        (Domain.MEDIA_TYPE, create_media_type_impediment_outcome),
        (Domain.BYTE_LENGTH, create_byte_length_impediment_outcome),
    ),
)
def test_impediment_is_rejected_before_exhaustive_set_construction(
    domain: SecurityAdmissionEvidenceDomain,
    factory: ResolutionFactory,
) -> None:
    source_outcome = factory()
    identity = create_coverage_identity(
        (domain,),
        source_outcome.coverage_identity,
    )
    outcome = rebind_outcome(source_outcome, identity)

    with pytest.raises(
        ValueError,
        match=(
            "outcomes must contain only resolved conclusive "
            "or indeterminate outcomes"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(outcome,),
        )


@pytest.mark.parametrize(
    "required_domains",
    (
        (Domain.MEDIA_TYPE,),
        (Domain.BYTE_LENGTH,),
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
        (Domain.BYTE_LENGTH, Domain.MEDIA_TYPE),
    ),
)
def test_exact_required_domain_order_is_accepted(
    required_domains: tuple[SecurityAdmissionEvidenceDomain, ...],
) -> None:
    outcome_set = create_set(required_domains)

    assert len(outcome_set.outcomes) == len(required_domains)


def test_reconstructed_equal_set_has_value_equality() -> None:
    outcome_set = create_set(
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
    )

    reconstructed = SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
        coverage_identity=replace(outcome_set.coverage_identity),
        outcomes=tuple(outcome_set.outcomes),
    )

    assert reconstructed == outcome_set
    assert reconstructed is not outcome_set


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            outcomes=(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, [], {}, object()),
)
def test_outcomes_requires_immutable_tuple(
    invalid_value: object,
) -> None:
    identity = create_coverage_identity((Domain.MEDIA_TYPE,))

    with pytest.raises(
        TypeError,
        match="outcomes must be an immutable tuple",
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=invalid_value,  # type: ignore[arg-type]
        )


def test_outcomes_must_not_be_empty() -> None:
    identity = create_coverage_identity((Domain.MEDIA_TYPE,))

    with pytest.raises(
        ValueError,
        match="outcomes must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_outcomes_reject_invalid_member_type(
    invalid_value: object,
) -> None:
    identity = create_coverage_identity((Domain.MEDIA_TYPE,))

    with pytest.raises(
        TypeError,
        match="outcomes must contain",
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(invalid_value,),  # type: ignore[arg-type]
        )


def test_different_coverage_occurrence_is_rejected() -> None:
    identity = create_coverage_identity((Domain.MEDIA_TYPE,))
    different_identity = replace(
        identity,
        coverage_version=identity.coverage_version + 1,
    )
    outcome = rebind_outcome(
        create_media_type_conclusive_outcome(),
        different_identity,
    )

    with pytest.raises(
        ValueError,
        match="each outcome must use the coverage identity",
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(outcome,),
        )


def test_missing_required_domain_is_rejected() -> None:
    identity = create_coverage_identity(
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
    )
    media_type = rebind_outcome(
        create_media_type_conclusive_outcome(),
        identity,
    )

    with pytest.raises(
        ValueError,
        match=(
            "outcome domains must exactly match "
            "required evidence domains"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(media_type,),
        )


def test_extra_domain_is_rejected() -> None:
    identity = create_coverage_identity((Domain.MEDIA_TYPE,))
    media_type = rebind_outcome(
        create_media_type_conclusive_outcome(),
        identity,
    )
    byte_length = rebind_outcome(
        create_byte_length_conclusive_outcome(),
        identity,
    )

    with pytest.raises(
        ValueError,
        match=(
            "outcome domains must exactly match "
            "required evidence domains"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(media_type, byte_length),
        )


def test_duplicate_domain_is_rejected() -> None:
    identity = create_coverage_identity(
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
    )
    first = rebind_outcome(
        create_media_type_conclusive_outcome(),
        identity,
    )
    second = rebind_outcome(
        create_media_type_indeterminate_outcome(),
        identity,
    )

    with pytest.raises(
        ValueError,
        match=(
            "outcome domains must exactly match "
            "required evidence domains"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(first, second),
        )


def test_wrong_domain_order_is_rejected() -> None:
    identity = create_coverage_identity(
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH)
    )
    media_type = rebind_outcome(
        create_media_type_conclusive_outcome(),
        identity,
    )
    byte_length = rebind_outcome(
        create_byte_length_conclusive_outcome(),
        identity,
    )

    with pytest.raises(
        ValueError,
        match=(
            "outcome domains must exactly match "
            "required evidence domains"
        ),
    ):
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
            coverage_identity=identity,
            outcomes=(byte_length, media_type),
        )


def test_decision_and_closure_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageResolutionOutcomeSet
        )
    }

    assert names.isdisjoint(
        {
            "coverage_status",
            "closure_status",
            "admission_decision",
            "rejection",
            "authority",
        }
    )


def test_contract_defines_validation_only() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet
    )
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
    outcome_set = create_set()

    for name in (
        "execute",
        "open",
        "send",
        "publish",
        "authorize",
        "admit",
        "reject",
        "close",
    ):
        assert not hasattr(outcome_set, name)
