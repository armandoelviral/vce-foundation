import ast
import inspect

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload
    as payload_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_ENCODING,
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)


def payload_bytes(
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> bytes:
    return (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )


def test_encoding_constant_is_exact() -> None:
    assert SECURITY_ADMISSION_MERKLE_CHECKPOINT_ENCODING == "UTF-8"


def test_payload_is_exact_utf8_serialization() -> None:
    checkpoint = create_checkpoint()

    expected = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        ).encode("UTF-8")
    )

    assert payload_bytes(checkpoint) == expected


def test_payload_has_exact_bytes_type() -> None:
    assert type(payload_bytes(create_checkpoint())) is bytes


def test_payload_is_deterministic() -> None:
    checkpoint = create_checkpoint()

    first = payload_bytes(checkpoint)
    second = payload_bytes(checkpoint)
    third = payload_bytes(checkpoint)

    assert first == second == third


def test_payload_decodes_to_exact_canonical_text() -> None:
    checkpoint = create_checkpoint()
    payload = payload_bytes(checkpoint)

    assert payload.decode("UTF-8") == (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )


def test_unicode_origin_uses_utf8_bytes() -> None:
    checkpoint = create_checkpoint(
        origin="admisión-segura",
    )
    payload = payload_bytes(checkpoint)

    assert "admisión-segura".encode("UTF-8") in payload
    assert b"\\u00f3" not in payload


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
def test_payload_preserves_checkpoint_state(
    origin: str,
    size: int,
) -> None:
    checkpoint = create_checkpoint(
        origin=origin,
        size=size,
    )
    payload = payload_bytes(checkpoint)

    assert origin.encode("UTF-8") in payload
    assert (
        f'"leaf_count":{size}'.encode("UTF-8")
        in payload
    )
    assert checkpoint.root.value.encode("UTF-8") in payload


def test_different_origin_produces_different_payload() -> None:
    first = payload_bytes(
        create_checkpoint(origin="origin-a")
    )
    second = payload_bytes(
        create_checkpoint(origin="origin-b")
    )

    assert first != second


def test_different_root_produces_different_payload() -> None:
    first = payload_bytes(create_checkpoint(size=2))
    second = payload_bytes(create_checkpoint(size=3))

    assert first != second


def test_payload_generation_does_not_mutate_checkpoint() -> None:
    checkpoint = create_checkpoint()
    origin = checkpoint.origin
    root = checkpoint.root

    payload_bytes(checkpoint)

    assert checkpoint.origin == origin
    assert checkpoint.root is root


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "checkpoint",
        b"checkpoint",
        {},
        object(),
    ),
)
def test_payload_requires_nominal_checkpoint(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        ),
    ):
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=invalid_value,  # type: ignore[arg-type]
        )


def test_payload_module_has_no_digest_or_signing_execution() -> None:
    source = inspect.getsource(payload_module)
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

    assert "hashlib" not in imported_names
    assert "hmac" not in imported_names
    assert "cryptography" not in imported_names
    assert "sign" not in called_names
    assert "verify" not in called_names


def test_payload_contains_domain_separation() -> None:
    payload = payload_bytes(create_checkpoint())

    assert (
        b"SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
        b"MERKLE-CHECKPOINT"
        in payload
    )


def test_payload_adds_no_signature_or_time_claim() -> None:
    payload = payload_bytes(create_checkpoint())

    assert b'"signature"' not in payload
    assert b'"key_id"' not in payload
    assert b'"timestamp"' not in payload
    assert b'"created_at"' not in payload
    assert b'"issued_at"' not in payload
