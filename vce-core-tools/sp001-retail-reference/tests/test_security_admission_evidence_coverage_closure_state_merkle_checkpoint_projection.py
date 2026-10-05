import ast
import inspect

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection
    as projection_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    create_root,
)


def create_checkpoint(
    *,
    origin: str = "sp001-security-admission",
    size: int = 3,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint:
    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin=origin,
            root=create_root(size),
        )
    )


def project(
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> dict[str, object]:
    return (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )


def test_projection_fields_are_exact() -> None:
    document = project(create_checkpoint())

    assert tuple(document) == (
        "domain",
        "origin",
        "root",
    )

    root_document = document["root"]

    assert isinstance(root_document, dict)
    assert tuple(root_document) == (
        "algorithm",
        "tree_hash_profile",
        "leaf_count",
        "value",
    )


def test_projection_values_are_exact() -> None:
    checkpoint = create_checkpoint()
    document = project(checkpoint)

    assert document == {
        "domain": (
            "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
            "MERKLE-CHECKPOINT"
        ),
        "origin": "sp001-security-admission",
        "root": {
            "algorithm": "SHA-256",
            "tree_hash_profile": "RFC6962",
            "leaf_count": 3,
            "value": checkpoint.root.value,
        },
    }


def test_projection_uses_declared_domain_constant() -> None:
    document = project(create_checkpoint())

    assert (
        document["domain"]
        == SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN
    )


@pytest.mark.parametrize(
    ("origin", "size"),
    (
        ("sp001-security-admission", 1),
        ("retail/security/admission", 2),
        ("urn:sp001:security-admission", 4),
        ("tenant-001", 7),
        ("admisión-segura", 9),
    ),
)
def test_projection_preserves_origin_and_root_state(
    origin: str,
    size: int,
) -> None:
    checkpoint = create_checkpoint(
        origin=origin,
        size=size,
    )

    document = project(checkpoint)
    root_document = document["root"]

    assert isinstance(root_document, dict)
    assert document["origin"] == origin
    assert root_document["leaf_count"] == size
    assert root_document["value"] == checkpoint.root.value


def test_projection_contains_only_json_native_values() -> None:
    document = project(create_checkpoint())
    root_document = document["root"]

    assert isinstance(document["domain"], str)
    assert isinstance(document["origin"], str)
    assert isinstance(root_document, dict)
    assert isinstance(root_document["algorithm"], str)
    assert isinstance(root_document["tree_hash_profile"], str)
    assert type(root_document["leaf_count"]) is int
    assert isinstance(root_document["value"], str)


def test_projection_returns_fresh_documents() -> None:
    checkpoint = create_checkpoint()

    first = project(checkpoint)
    second = project(checkpoint)

    assert first == second
    assert first is not second
    assert first["root"] is not second["root"]


def test_projected_document_mutation_does_not_change_checkpoint() -> None:
    checkpoint = create_checkpoint()
    document = project(checkpoint)
    root_document = document["root"]

    assert isinstance(root_document, dict)

    document["origin"] = "changed"
    root_document["leaf_count"] = 999
    root_document["value"] = "0" * 64

    assert checkpoint.origin == "sp001-security-admission"
    assert checkpoint.root.leaf_count == 3
    assert checkpoint.root.value != "0" * 64


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "checkpoint",
        {},
        object(),
    ),
)
def test_projection_requires_nominal_checkpoint(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        ),
    ):
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=invalid_value,  # type: ignore[arg-type]
        )


def test_projection_has_no_signing_execution() -> None:
    source = inspect.getsource(projection_module)
    tree = ast.parse(source)

    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
        )
    }

    assert "cryptography" not in imported_names
    assert "hmac" not in imported_names
    assert "sign" not in called_names
    assert "verify" not in called_names


def test_projection_adds_no_time_decision_or_authority_claims() -> None:
    document = project(create_checkpoint())

    forbidden = {
        "timestamp",
        "created_at",
        "issued_at",
        "signature",
        "key_id",
        "decision",
        "authority",
        "authorization",
    }

    assert forbidden.isdisjoint(document)
