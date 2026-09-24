import ast
import inspect
from dataclasses import replace
from typing import Callable

import pytest

from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_closure_impediment import (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_coverage_closure_resolution import (
    resolve_security_admission_evidence_coverage_closure,
)
from tests.test_security_admission_evidence_coverage_closure_blockage import (
    rebind_impediment,
)
from tests.test_security_admission_evidence_coverage_resolution_outcome_set import (
    create_byte_length_conclusive_outcome,
    create_byte_length_impediment_outcome,
    create_byte_length_indeterminate_outcome,
    create_coverage_identity,
    create_media_type_conclusive_outcome,
    create_media_type_impediment_outcome,
    create_media_type_indeterminate_outcome,
    rebind_outcome,
)


Domain = SecurityAdmissionEvidenceDomain
ResolutionOutcome = (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
    | SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome
)
OutcomeFactory = Callable[[], ResolutionOutcome]


def rebind_execution_outcome(
    outcome: ResolutionOutcome,
    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
) -> ResolutionOutcome:
    if isinstance(
        outcome.outcome,
        (
            SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
            SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
        ),
    ):
        return replace(
            outcome,
            coverage_identity=coverage_identity,
            outcome=rebind_impediment(
                outcome.outcome,
                coverage_identity,
            ),
        )
    return rebind_outcome(outcome, coverage_identity)


def create_execution(
    required_domains: tuple[Domain, ...],
    factories: tuple[OutcomeFactory, ...],
) -> tuple[
    SecurityAdmissionEvidenceCoverageIdentity,
    tuple[ResolutionOutcome, ...],
]:
    initial = factories[0]()
    coverage_identity = create_coverage_identity(
        required_domains,
        initial.coverage_identity,
    )
    outcomes = tuple(
        rebind_execution_outcome(
            factory(),
            coverage_identity,
        )
        for factory in factories
    )
    return coverage_identity, outcomes


def create_resolver(
    name: str,
    outcome: ResolutionOutcome,
    calls: list[tuple[str, SecurityAdmissionEvidenceCoverageIdentity]],
) -> Callable[
    [SecurityAdmissionEvidenceCoverageIdentity],
    ResolutionOutcome,
]:
    def resolve(
        coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
    ) -> ResolutionOutcome:
        calls.append((name, coverage_identity))
        return outcome

    return resolve


def forbidden_resolver(
    name: str,
    calls: list[tuple[str, SecurityAdmissionEvidenceCoverageIdentity]],
) -> Callable[[SecurityAdmissionEvidenceCoverageIdentity], ResolutionOutcome]:
    def resolve(
        coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
    ) -> ResolutionOutcome:
        calls.append((name, coverage_identity))
        raise AssertionError(f"{name} resolver must not be called")

    return resolve


@pytest.mark.parametrize(
    ("domain", "factory", "called_name", "forbidden_name"),
    (
        (
            Domain.MEDIA_TYPE,
            create_media_type_impediment_outcome,
            "media_type",
            "byte_length",
        ),
        (
            Domain.BYTE_LENGTH,
            create_byte_length_impediment_outcome,
            "byte_length",
            "media_type",
        ),
    ),
)
def test_first_impediment_stops_before_other_resolver(
    domain: Domain,
    factory: OutcomeFactory,
    called_name: str,
    forbidden_name: str,
) -> None:
    coverage_identity, outcomes = create_execution(
        (domain,),
        (factory,),
    )
    calls: list[
        tuple[str, SecurityAdmissionEvidenceCoverageIdentity]
    ] = []
    called = create_resolver(called_name, outcomes[0], calls)
    forbidden = forbidden_resolver(forbidden_name, calls)

    resolution = resolve_security_admission_evidence_coverage_closure(
        coverage_identity=coverage_identity,
        media_type_resolver=(
            called if domain is Domain.MEDIA_TYPE else forbidden
        ),
        byte_length_resolver=(
            called if domain is Domain.BYTE_LENGTH else forbidden
        ),
    )

    assert isinstance(
        resolution.outcome,
        SecurityAdmissionEvidenceCoverageClosureBlockage,
    )
    assert resolution.outcome.resolved_prefix == ()
    assert resolution.outcome.impediment is outcomes[0].outcome
    assert calls == [(called_name, coverage_identity)]


@pytest.mark.parametrize(
    (
        "required_domains",
        "factories",
        "expected_calls",
    ),
    (
        (
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
            (
                create_media_type_conclusive_outcome,
                create_byte_length_impediment_outcome,
            ),
            ("media_type", "byte_length"),
        ),
        (
            (Domain.BYTE_LENGTH, Domain.MEDIA_TYPE),
            (
                create_byte_length_conclusive_outcome,
                create_media_type_impediment_outcome,
            ),
            ("byte_length", "media_type"),
        ),
    ),
)
def test_second_domain_impediment_preserves_only_resolved_prefix(
    required_domains: tuple[Domain, ...],
    factories: tuple[OutcomeFactory, ...],
    expected_calls: tuple[str, ...],
) -> None:
    coverage_identity, outcomes = create_execution(
        required_domains,
        factories,
    )
    calls: list[
        tuple[str, SecurityAdmissionEvidenceCoverageIdentity]
    ] = []
    media_outcome = next(
        outcome
        for outcome in outcomes
        if isinstance(
            outcome,
            SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
        )
    )
    byte_outcome = next(
        outcome
        for outcome in outcomes
        if isinstance(
            outcome,
            SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
        )
    )

    resolution = resolve_security_admission_evidence_coverage_closure(
        coverage_identity=coverage_identity,
        media_type_resolver=create_resolver(
            "media_type",
            media_outcome,
            calls,
        ),
        byte_length_resolver=create_resolver(
            "byte_length",
            byte_outcome,
            calls,
        ),
    )

    assert isinstance(
        resolution.outcome,
        SecurityAdmissionEvidenceCoverageClosureBlockage,
    )
    assert resolution.outcome.resolved_prefix == (outcomes[0],)
    assert resolution.outcome.impediment is outcomes[1].outcome
    assert tuple(name for name, _ in calls) == expected_calls
    assert all(
        identity is coverage_identity
        for _, identity in calls
    )


@pytest.mark.parametrize(
    ("required_domains", "factories", "expected_calls"),
    (
        (
            (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
            (
                create_media_type_conclusive_outcome,
                create_byte_length_indeterminate_outcome,
            ),
            ("media_type", "byte_length"),
        ),
        (
            (Domain.BYTE_LENGTH, Domain.MEDIA_TYPE),
            (
                create_byte_length_indeterminate_outcome,
                create_media_type_conclusive_outcome,
            ),
            ("byte_length", "media_type"),
        ),
    ),
)
def test_all_resolved_domains_create_complete_closure(
    required_domains: tuple[Domain, ...],
    factories: tuple[OutcomeFactory, ...],
    expected_calls: tuple[str, ...],
) -> None:
    coverage_identity, outcomes = create_execution(
        required_domains,
        factories,
    )
    calls: list[
        tuple[str, SecurityAdmissionEvidenceCoverageIdentity]
    ] = []
    media_outcome = next(
        outcome
        for outcome in outcomes
        if isinstance(
            outcome,
            SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
        )
    )
    byte_outcome = next(
        outcome
        for outcome in outcomes
        if isinstance(
            outcome,
            SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
        )
    )

    resolution = resolve_security_admission_evidence_coverage_closure(
        coverage_identity=coverage_identity,
        media_type_resolver=create_resolver(
            "media_type",
            media_outcome,
            calls,
        ),
        byte_length_resolver=create_resolver(
            "byte_length",
            byte_outcome,
            calls,
        ),
    )

    assert isinstance(
        resolution.outcome,
        SecurityAdmissionEvidenceCoverageClosure,
    )
    assert (
        resolution.outcome.resolution_outcome_set.outcomes
        == outcomes
    )
    assert tuple(name for name, _ in calls) == expected_calls
    assert all(
        identity is coverage_identity
        for _, identity in calls
    )


@pytest.mark.parametrize(
    ("domain", "factory"),
    (
        (Domain.MEDIA_TYPE, create_media_type_indeterminate_outcome),
        (Domain.BYTE_LENGTH, create_byte_length_indeterminate_outcome),
    ),
)
def test_indeterminate_domain_is_resolved_not_blocked(
    domain: Domain,
    factory: OutcomeFactory,
) -> None:
    coverage_identity, outcomes = create_execution(
        (domain,),
        (factory,),
    )
    calls: list[
        tuple[str, SecurityAdmissionEvidenceCoverageIdentity]
    ] = []
    active = create_resolver("active", outcomes[0], calls)
    forbidden = forbidden_resolver("forbidden", calls)

    resolution = resolve_security_admission_evidence_coverage_closure(
        coverage_identity,
        active if domain is Domain.MEDIA_TYPE else forbidden,
        active if domain is Domain.BYTE_LENGTH else forbidden,
    )

    assert isinstance(
        resolution.outcome,
        SecurityAdmissionEvidenceCoverageClosure,
    )
    assert (
        resolution.outcome.resolution_outcome_set.outcomes
        == outcomes
    )
    assert len(calls) == 1


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        ),
    ):
        resolve_security_admission_evidence_coverage_closure(
            invalid_value,  # type: ignore[arg-type]
            lambda _: create_media_type_conclusive_outcome(),
            lambda _: create_byte_length_conclusive_outcome(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_media_type_resolver_must_be_callable(
    invalid_value: object,
) -> None:
    coverage_identity, _ = create_execution(
        (Domain.MEDIA_TYPE,),
        (create_media_type_conclusive_outcome,),
    )
    with pytest.raises(
        TypeError,
        match="media_type_resolver must be callable",
    ):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            invalid_value,  # type: ignore[arg-type]
            lambda _: create_byte_length_conclusive_outcome(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_byte_length_resolver_must_be_callable(
    invalid_value: object,
) -> None:
    coverage_identity, _ = create_execution(
        (Domain.BYTE_LENGTH,),
        (create_byte_length_conclusive_outcome,),
    )
    with pytest.raises(
        TypeError,
        match="byte_length_resolver must be callable",
    ):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            lambda _: create_media_type_conclusive_outcome(),
            invalid_value,  # type: ignore[arg-type]
        )


def test_media_type_resolver_requires_media_type_outcome() -> None:
    coverage_identity, outcomes = create_execution(
        (Domain.MEDIA_TYPE,),
        (create_byte_length_conclusive_outcome,),
    )
    with pytest.raises(
        TypeError,
        match=(
            "media_type_resolver must return a "
            "SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome"
        ),
    ):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            lambda _: outcomes[0],
            lambda _: outcomes[0],
        )


def test_byte_length_resolver_requires_byte_length_outcome() -> None:
    coverage_identity, outcomes = create_execution(
        (Domain.BYTE_LENGTH,),
        (create_media_type_conclusive_outcome,),
    )
    with pytest.raises(
        TypeError,
        match=(
            "byte_length_resolver must return a "
            "SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome"
        ),
    ):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            lambda _: outcomes[0],
            lambda _: outcomes[0],
        )


def test_different_coverage_outcome_is_rejected() -> None:
    coverage_identity, outcomes = create_execution(
        (Domain.MEDIA_TYPE,),
        (create_media_type_conclusive_outcome,),
    )
    different_identity = replace(
        coverage_identity,
        coverage_version=coverage_identity.coverage_version + 1,
    )
    different_outcome = rebind_outcome(
        outcomes[0],
        different_identity,
    )

    with pytest.raises(
        ValueError,
        match=(
            "resolved domain outcome must use "
            "the exact coverage identity"
        ),
    ):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            lambda _: different_outcome,
            lambda _: create_byte_length_conclusive_outcome(),
        )


def test_resolver_failure_propagates_without_later_call() -> None:
    coverage_identity, _ = create_execution(
        (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
        (
            create_media_type_conclusive_outcome,
            create_byte_length_conclusive_outcome,
        ),
    )
    calls: list[str] = []

    def fail(
        _: SecurityAdmissionEvidenceCoverageIdentity,
    ) -> SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome:
        calls.append("media_type")
        raise RuntimeError("resolver failure")

    def forbidden(
        _: SecurityAdmissionEvidenceCoverageIdentity,
    ) -> SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome:
        calls.append("byte_length")
        raise AssertionError("later resolver must not be called")

    with pytest.raises(RuntimeError, match="resolver failure"):
        resolve_security_admission_evidence_coverage_closure(
            coverage_identity,
            fail,
            forbidden,
        )

    assert calls == ["media_type"]


def test_service_contains_explicit_fail_fast_return() -> None:
    source = inspect.getsource(
        resolve_security_admission_evidence_coverage_closure
    )
    tree = ast.parse(source)
    loops = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.For)
    ]
    assert len(loops) == 1
    assert any(
        isinstance(node, ast.Return)
        for node in ast.walk(loops[0])
    )


def test_service_does_not_define_assessment_or_decision_semantics() -> None:
    source = inspect.getsource(
        resolve_security_admission_evidence_coverage_closure
    )
    for forbidden_name in (
        "assessment",
        "classification",
        "admission_decision",
        "rejection",
        "authority",
    ):
        assert forbidden_name not in source


def test_service_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        resolve_security_admission_evidence_coverage_closure
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"collections", "sp001"}
