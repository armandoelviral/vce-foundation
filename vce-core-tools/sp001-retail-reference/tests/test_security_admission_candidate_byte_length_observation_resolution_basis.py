import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_basis import (
    SecurityAdmissionCandidateByteLengthObservationResolutionBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_set import (
    SecurityAdmissionCandidateByteLengthObservationSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.contracts.security_admission_policy_verification_procedure_authority_order import (
    SecurityAdmissionPolicyVerificationProcedureAuthorityOrder,
)
from tests.test_security_admission_candidate_byte_length_observation_set import (
    create_set,
)
from tests.test_security_admission_policy_verification_procedure_authority_order import (
    create_order,
)


def create_basis(
) -> SecurityAdmissionCandidateByteLengthObservationResolutionBasis:
    observation_set = create_set()
    observed_procedure = (
        observation_set.observations[0].verification_procedure_identity
    )
    secondary_procedure = (
        create_order().verification_procedure_identities[0]
    )
    authority_order = replace(
        create_order(),
        evidence_domain=SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
        verification_procedure_identities=(
            observed_procedure,
            secondary_procedure,
        ),
    )
    return SecurityAdmissionCandidateByteLengthObservationResolutionBasis(
        observation_set=observation_set,
        authority_order=authority_order,
    )

def test_fields_are_exact() -> None:
    basis_fields = fields(
        SecurityAdmissionCandidateByteLengthObservationResolutionBasis
    )
    assert tuple(field.name for field in basis_fields) == (
        "observation_set",
        "authority_order",
    )
    assert (
        basis_fields[0].type
        is SecurityAdmissionCandidateByteLengthObservationSet
    )
    assert (
        basis_fields[1].type
        is SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
    )


def test_basis_is_immutable_and_slotted() -> None:
    basis = create_basis()
    assert not hasattr(basis, "__dict__")
    with pytest.raises(FrozenInstanceError):
        basis.observation_set = create_set()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    observation_set = create_set()
    observed_procedure = (
        observation_set.observations[0].verification_procedure_identity
    )
    authority_order = replace(
        create_order(),
        evidence_domain=SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
        verification_procedure_identities=(
            observed_procedure,
            create_order().verification_procedure_identities[0],
        ),
    )
    basis = SecurityAdmissionCandidateByteLengthObservationResolutionBasis(
        observation_set=observation_set,
        authority_order=authority_order,
    )
    assert basis.observation_set is observation_set
    assert basis.authority_order is authority_order

def test_equal_reconstruction_has_value_equality() -> None:
    basis = create_basis()
    reconstructed = replace(
        basis,
        observation_set=replace(basis.observation_set),
        authority_order=replace(basis.authority_order),
    )
    assert reconstructed == basis
    assert reconstructed is not basis


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_observation_set_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "observation_set must be a "
            "SecurityAdmissionCandidateByteLengthObservationSet"
        ),
    ):
        replace(
            create_basis(),
            observation_set=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_authority_order_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "authority_order must be a "
            "SecurityAdmissionPolicyVerificationProcedureAuthorityOrder"
        ),
    ):
        replace(
            create_basis(),
            authority_order=invalid_value,  # type: ignore[arg-type]
        )


def test_non_byte_length_authority_order_is_rejected() -> None:
    basis = create_basis()
    byte_length_order = replace(
        basis.authority_order,
        evidence_domain=SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
    )
    with pytest.raises(
        ValueError,
        match=(
            "authority_order must govern the BYTE_LENGTH evidence domain"
        ),
    ):
        replace(basis, authority_order=byte_length_order)


def test_policy_version_participates_in_basis_value() -> None:
    basis = create_basis()
    changed_policy = replace(
        basis.authority_order.admission_policy_identity,
        admission_policy_version=(
            basis.authority_order
            .admission_policy_identity
            .admission_policy_version
            + 1
        ),
    )
    changed_order = replace(
        basis.authority_order,
        admission_policy_identity=changed_policy,
    )
    assert replace(basis, authority_order=changed_order) != basis


def test_authority_precedence_participates_in_basis_value() -> None:
    basis = create_basis()
    reversed_order = replace(
        basis.authority_order,
        verification_procedure_identities=tuple(
            reversed(
                basis.authority_order.verification_procedure_identities
            )
        ),
    )
    assert replace(basis, authority_order=reversed_order) != basis


def test_observation_set_version_participates_in_basis_value() -> None:
    basis = create_basis()
    changed_set = replace(
        basis.observation_set,
        observation_set_version=(
            basis.observation_set.observation_set_version + 1
        ),
    )
    assert replace(basis, observation_set=changed_set) != basis


def test_basis_does_not_require_procedure_membership_yet() -> None:
    basis = create_basis()
    unrelated_order = replace(
        basis.authority_order,
        verification_procedure_identities=(
            create_order().verification_procedure_identities[0],
        ),
    )
    preserved = replace(basis, authority_order=unrelated_order)
    assert preserved.authority_order is unrelated_order


def test_resolution_and_admission_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthObservationResolutionBasis
        )
    }
    assert names.isdisjoint({
        "selected_observation",
        "conflict_reason",
        "resolved_at",
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthObservationResolutionBasis
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
        SecurityAdmissionCandidateByteLengthObservationResolutionBasis
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
