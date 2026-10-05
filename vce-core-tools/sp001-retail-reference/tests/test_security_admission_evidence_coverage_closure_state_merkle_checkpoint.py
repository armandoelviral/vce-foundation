import ast
import inspect
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_merkle_checkpoint
    as checkpoint_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    build_security_admission_evidence_coverage_closure_state_merkle_root,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_root import (
    manifest_with_size,
)


def create_root(
    size: int = 3,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot:
    return (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest_with_size(size),
        )
    )


def create_checkpoint(
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint:
    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin="sp001-security-admission",
            root=create_root(),
        )
    )


def test_checkpoint_fields_are_exact() -> None:
    checkpoint_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
    )

    assert tuple(field.name for field in checkpoint_fields) == (
        "origin",
        "root",
    )
    assert tuple(field.type for field in checkpoint_fields) == (
        str,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    )


def test_checkpoint_is_immutable_and_slotted() -> None:
    checkpoint = create_checkpoint()

    assert not hasattr(checkpoint, "__dict__")

    with pytest.raises(FrozenInstanceError):
        checkpoint.origin = "changed"  # type: ignore[misc]


def test_checkpoint_domain_is_exact() -> None:
    assert SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN == (
        "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
        "MERKLE-CHECKPOINT"
    )


def test_exact_root_reference_is_preserved() -> None:
    root = create_root()

    checkpoint = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin="sp001-security-admission",
            root=root,
        )
    )

    assert checkpoint.root is root
    assert checkpoint.origin == "sp001-security-admission"


@pytest.mark.parametrize(
    "origin",
    (
        "sp001-security-admission",
        "retail/security/admission",
        "urn:sp001:security-admission",
        "tenant-001",
    ),
)
def test_nonempty_canonical_origins_are_preserved(
    origin: str,
) -> None:
    checkpoint = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin=origin,
            root=create_root(),
        )
    )

    assert checkpoint.origin == origin


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"sp001",
        object(),
    ),
)
def test_origin_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="origin must be a str",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin=invalid_value,  # type: ignore[arg-type]
            root=create_root(),
        )


def test_origin_rejects_empty_string() -> None:
    with pytest.raises(
        ValueError,
        match="origin must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin="",
            root=create_root(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        " ",
        "\t",
        "\n",
        " sp001",
        "sp001 ",
        "\tsp001",
        "sp001\n",
    ),
)
def test_origin_rejects_surrounding_whitespace(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "origin must not contain surrounding whitespace"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin=invalid_value,
            root=create_root(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "root",
        object(),
    ),
)
def test_root_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "root must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin="sp001-security-admission",
            root=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        4,
        7,
        8,
        9,
    ),
)
def test_checkpoint_preserves_every_valid_tree_size(
    size: int,
) -> None:
    root = create_root(size)

    checkpoint = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin="sp001-security-admission",
            root=root,
        )
    )

    assert checkpoint.root.leaf_count == size
    assert checkpoint.root.value == root.value


def test_checkpoint_defines_no_signature_material() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
        )
    }

    assert "signature" not in field_names
    assert "private_key" not in field_names
    assert "public_key" not in field_names
    assert "key_id" not in field_names


def test_checkpoint_defines_no_untrusted_time_claim() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
        )
    }

    assert "timestamp" not in field_names
    assert "created_at" not in field_names
    assert "issued_at" not in field_names


def test_checkpoint_module_has_no_signing_execution() -> None:
    source = inspect.getsource(checkpoint_module)
    tree = ast.parse(source)

    function_names = {
        node.name
        for node in tree.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "sign" not in function_names
    assert "verify" not in function_names
    assert "cryptography" not in imported_names
    assert "hmac" not in imported_names


def test_checkpoint_has_no_decision_or_authority_fields() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
        )
    }

    assert "decision" not in field_names
    assert "admission_status" not in field_names
    assert "authority" not in field_names
    assert "authorization" not in field_names
