import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)
from sp001.contracts.security_admission_policy_verification_procedure_authority_order import (
    SecurityAdmissionPolicyVerificationProcedureAuthorityOrder,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=value,
    )


def create_policy() -> SecurityAdmissionPolicyIdentity:
    return SecurityAdmissionPolicyIdentity(
        admission_policy_id="policy-001",
        admission_policy_version=1,
        configuration_digest=create_digest("0" * 64),
    )


def create_procedure(
    procedure_id: str = "procedure-001",
    verifier_id: str = "metadata-verifier-primary",
    verifier_version: str = "v1",
    digest_value: str = "1" * 64,
) -> SecurityAdmissionMetadataVerificationProcedureIdentity:
    return SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id=procedure_id,
        verifier_id=verifier_id,
        verifier_version=verifier_version,
        configuration_digest=create_digest(digest_value),
    )


def create_order(
) -> SecurityAdmissionPolicyVerificationProcedureAuthorityOrder:
    primary = create_procedure()
    secondary = create_procedure(
        procedure_id="procedure-002",
        verifier_id="metadata-verifier-secondary",
        verifier_version="v2",
        digest_value="2" * 64,
    )
    return SecurityAdmissionPolicyVerificationProcedureAuthorityOrder(
        admission_policy_identity=create_policy(),
        evidence_domain=SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
        verification_procedure_identities=(primary, secondary),
    )


def test_fields_are_exact() -> None:
    authority_fields = fields(
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
    )
    assert tuple(field.name for field in authority_fields) == (
        "admission_policy_identity",
        "evidence_domain",
        "verification_procedure_identities",
    )
    assert authority_fields[0].type is SecurityAdmissionPolicyIdentity
    assert authority_fields[1].type is SecurityAdmissionEvidenceDomain


def test_order_is_immutable_and_slotted() -> None:
    authority_order = create_order()
    assert not hasattr(authority_order, "__dict__")
    with pytest.raises(FrozenInstanceError):
        authority_order.evidence_domain = (  # type: ignore[misc]
            SecurityAdmissionEvidenceDomain.BYTE_LENGTH
        )


def test_exact_references_and_declared_order_are_preserved() -> None:
    policy = create_policy()
    primary = create_procedure()
    secondary = create_procedure(
        procedure_id="procedure-002",
        verifier_id="secondary",
        verifier_version="v2",
        digest_value="2" * 64,
    )
    procedures = (primary, secondary)
    authority_order = (
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder(
            admission_policy_identity=policy,
            evidence_domain=SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
            verification_procedure_identities=procedures,
        )
    )
    assert authority_order.admission_policy_identity is policy
    assert authority_order.verification_procedure_identities is procedures
    assert authority_order.verification_procedure_identities[0] is primary
    assert authority_order.verification_procedure_identities[1] is secondary


def test_equal_reconstruction_has_value_equality() -> None:
    authority_order = create_order()
    reconstructed = replace(
        authority_order,
        admission_policy_identity=replace(
            authority_order.admission_policy_identity
        ),
        verification_procedure_identities=tuple(
            replace(identity)
            for identity in authority_order.verification_procedure_identities
        ),
    )
    assert reconstructed == authority_order
    assert reconstructed is not authority_order


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_policy_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "admission_policy_identity must be a "
            "SecurityAdmissionPolicyIdentity"
        ),
    ):
        replace(
            create_order(),
            admission_policy_identity=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, "MEDIA_TYPE", 1, object()))
def test_evidence_domain_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evidence_domain must be a "
            "SecurityAdmissionEvidenceDomain"
        ),
    ):
        replace(
            create_order(),
            evidence_domain=invalid_value,  # type: ignore[arg-type]
        )


def test_each_closed_evidence_domain_is_preserved() -> None:
    media_order = create_order()
    byte_order = replace(
        media_order,
        evidence_domain=SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
    )
    assert (
        media_order.evidence_domain
        is SecurityAdmissionEvidenceDomain.MEDIA_TYPE
    )
    assert (
        byte_order.evidence_domain
        is SecurityAdmissionEvidenceDomain.BYTE_LENGTH
    )


@pytest.mark.parametrize("invalid_value", (None, [], {}, set()))
def test_procedure_identities_require_tuple(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "verification_procedure_identities must be an immutable tuple"
        ),
    ):
        replace(
            create_order(),
            verification_procedure_identities=invalid_value,  # type: ignore[arg-type]
        )


def test_procedure_identities_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="verification_procedure_identities must not be empty",
    ):
        replace(
            create_order(),
            verification_procedure_identities=(),
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_each_procedure_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "verification_procedure_identities must contain "
            "SecurityAdmissionMetadataVerificationProcedureIdentity values"
        ),
    ):
        replace(
            create_order(),
            verification_procedure_identities=(
                invalid_value,  # type: ignore[arg-type]
            ),
        )


def test_duplicate_exact_procedure_identity_is_rejected() -> None:
    identity = create_procedure()
    with pytest.raises(
        ValueError,
        match="duplicate verification procedure identity",
    ):
        replace(
            create_order(),
            verification_procedure_identities=(identity, replace(identity)),
        )


def test_distinct_versions_of_one_procedure_id_are_permitted() -> None:
    first = create_procedure()
    second = replace(first, verifier_version="v2")
    authority_order = replace(
        create_order(),
        verification_procedure_identities=(first, second),
    )
    assert authority_order.verification_procedure_identities == (
        first,
        second,
    )


def test_distinct_configurations_of_one_procedure_id_are_permitted() -> None:
    first = create_procedure()
    second = replace(
        first,
        configuration_digest=create_digest("3" * 64),
    )
    authority_order = replace(
        create_order(),
        verification_procedure_identities=(first, second),
    )
    assert authority_order.verification_procedure_identities == (
        first,
        second,
    )


def test_reversing_declared_precedence_changes_value() -> None:
    authority_order = create_order()
    reversed_order = replace(
        authority_order,
        verification_procedure_identities=tuple(
            reversed(authority_order.verification_procedure_identities)
        ),
    )
    assert reversed_order != authority_order
    assert (
        reversed_order.verification_procedure_identities[0]
        is authority_order.verification_procedure_identities[1]
    )


def test_policy_domain_and_procedures_participate_in_value() -> None:
    authority_order = create_order()
    changed_policy = replace(
        authority_order.admission_policy_identity,
        admission_policy_version=2,
    )
    changed_domain = replace(
        authority_order,
        evidence_domain=SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
    )
    changed_procedure = replace(
        authority_order.verification_procedure_identities[0],
        verifier_version="v9",
    )
    changed_procedures = replace(
        authority_order,
        verification_procedure_identities=(
            changed_procedure,
            authority_order.verification_procedure_identities[1],
        ),
    )
    assert replace(
        authority_order,
        admission_policy_identity=changed_policy,
    ) != authority_order
    assert changed_domain != authority_order
    assert changed_procedures != authority_order


def test_resolution_decision_and_external_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
        )
    }
    assert names.isdisjoint({
        "selected_observation",
        "winning_observation",
        "comparison_result",
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
        "authorization",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
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
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
