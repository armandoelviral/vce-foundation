from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)

UINT64_MAX = (1 << 64) - 1

CHECKPOINT_SERIALIZATION = (
    '{"domain":"SP001-SECURITY-ADMISSION-CLOSURE-STATE-'
    'MERKLE-CHECKPOINT","origin":"sp001-security-admission",'
    '"root":{"algorithm":"SHA-256","leaf_count":3,'
    '"tree_hash_profile":"RFC6962","value":"'
    + ("a" * 64)
    + '"}}'
)


def create_stored_state(
    **changes: object,
) -> StoredState:
    values = {
        "storage_schema_version": 1,
        "publication_id": "publication-001",
        "checkpoint_serialization": CHECKPOINT_SERIALIZATION,
        "signing_key_id": "kms://security/key-001",
        "signing_algorithm": "ECDSA-P256-SHA256",
        "public_key_encoding": "DER-SPKI",
        "public_key_fingerprint": "b" * 64,
        "signature_encoding": "ASN.1-DER",
        "signature": b"signature",
        "phase": Phase.INTENT_RECORDED.value,
        "revision": 1,
    }
    values.update(changes)

    return StoredState(**values)


def test_storage_schema_version_constant_is_exact() -> None:
    assert (
        SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION
        == 1
    )


def test_stored_state_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(StoredState)
    ) == (
        "storage_schema_version",
        "publication_id",
        "checkpoint_serialization",
        "signing_key_id",
        "signing_algorithm",
        "public_key_encoding",
        "public_key_fingerprint",
        "signature_encoding",
        "signature",
        "phase",
        "revision",
    )


def test_stored_state_preserves_exact_values() -> None:
    signature = b"\x30\x06\x02\x01\x01\x02\x01\x01"

    stored = create_stored_state(
        publication_id="tenant://mx/publication-007",
        signature=signature,
        phase=Phase.COMMIT_DECIDED.value,
        revision=19,
    )

    assert stored.storage_schema_version == 1
    assert stored.publication_id == (
        "tenant://mx/publication-007"
    )
    assert stored.checkpoint_serialization == (
        CHECKPOINT_SERIALIZATION
    )
    assert stored.signing_key_id == (
        "kms://security/key-001"
    )
    assert stored.signing_algorithm == (
        "ECDSA-P256-SHA256"
    )
    assert stored.public_key_encoding == "DER-SPKI"
    assert stored.public_key_fingerprint == "b" * 64
    assert stored.signature_encoding == "ASN.1-DER"
    assert stored.signature is signature
    assert stored.phase == Phase.COMMIT_DECIDED.value
    assert stored.revision == 19


@pytest.mark.parametrize("phase", tuple(Phase))
def test_every_supported_phase_value_is_preserved(
    phase: Phase,
) -> None:
    stored = create_stored_state(
        phase=phase.value,
    )

    assert stored.phase == phase.value
    assert type(stored.phase) is str


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        7,
        65537,
        UINT64_MAX,
    ),
)
def test_positive_uint64_revisions_are_preserved(
    revision: int,
) -> None:
    stored = create_stored_state(
        revision=revision,
    )

    assert stored.revision == revision


@pytest.mark.parametrize(
    "attribute,value",
    (
        ("storage_schema_version", 2),
        ("publication_id", "changed"),
        ("checkpoint_serialization", "{}"),
        ("signing_key_id", "changed"),
        ("signing_algorithm", "changed"),
        ("public_key_encoding", "changed"),
        ("public_key_fingerprint", "c" * 64),
        ("signature_encoding", "changed"),
        ("signature", b"changed"),
        ("phase", Phase.PREPARED.value),
        ("revision", 2),
    ),
)
def test_stored_state_is_frozen(
    attribute: str,
    value: object,
) -> None:
    stored = create_stored_state()

    with pytest.raises(FrozenInstanceError):
        setattr(stored, attribute, value)


def test_stored_state_uses_slots() -> None:
    stored = create_stored_state()

    assert not hasattr(stored, "__dict__")
    assert StoredState.__slots__ == tuple(
        field.name
        for field in fields(StoredState)
    )


def test_equal_primitive_values_are_equal() -> None:
    assert create_stored_state() == create_stored_state()


def test_different_primitive_values_are_not_equal() -> None:
    assert create_stored_state() != create_stored_state(
        revision=2,
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        (),
    ),
)
def test_storage_schema_version_requires_exact_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="storage_schema_version",
    ):
        create_stored_state(
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        UINT64_MAX + 1,
    ),
)
def test_storage_schema_version_requires_positive_uint64(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="storage_schema_version",
    ):
        create_stored_state(
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        2,
        3,
        UINT64_MAX,
    ),
)
def test_unknown_storage_schema_version_fails_closed(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="storage_schema_version is not supported",
    ):
        create_stored_state(
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "publication_id",
        "checkpoint_serialization",
        "signing_key_id",
        "signing_algorithm",
        "public_key_encoding",
        "signature_encoding",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        1,
        b"value",
        (),
    ),
)
def test_text_fields_require_exact_string(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        create_stored_state(
            **{field_name: value},
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "publication_id",
        "checkpoint_serialization",
        "signing_key_id",
        "signing_algorithm",
        "public_key_encoding",
        "signature_encoding",
    ),
)
def test_text_fields_reject_empty_value(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty",
    ):
        create_stored_state(
            **{field_name: ""},
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        1,
        b"a" * 64,
        "",
        "a" * 63,
        "a" * 65,
        "A" * 64,
        "g" * 64,
    ),
)
def test_public_key_fingerprint_requires_lower_hex_sha256(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "public_key_fingerprint must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        create_stored_state(
            public_key_fingerprint=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "signature",
        bytearray(b"signature"),
        memoryview(b"signature"),
        1,
        (),
    ),
)
def test_signature_requires_exact_bytes(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="signature must be bytes",
    ):
        create_stored_state(signature=value)


def test_signature_rejects_empty_bytes() -> None:
    with pytest.raises(
        ValueError,
        match="signature must not be empty",
    ):
        create_stored_state(signature=b"")


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        1,
        b"PREPARED",
        (),
    ),
)
def test_phase_requires_exact_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="phase must be a string",
    ):
        create_stored_state(phase=value)


@pytest.mark.parametrize(
    "value",
    (
        "",
        "UNKNOWN",
        "prepared",
        "COMMIT",
        "ABORT",
    ),
)
def test_phase_rejects_unsupported_value(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "phase must be a supported publication phase"
        ),
    ):
        create_stored_state(phase=value)


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        (),
    ),
)
def test_revision_requires_exact_integer(
    value: object,
) -> None:
    with pytest.raises(TypeError, match="revision"):
        create_stored_state(revision=value)


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        UINT64_MAX + 1,
    ),
)
def test_revision_requires_positive_uint64(
    value: int,
) -> None:
    with pytest.raises(ValueError, match="revision"):
        create_stored_state(revision=value)


def test_record_does_not_parse_or_execute_checkpoint() -> None:
    stored = create_stored_state(
        checkpoint_serialization="{not-json}",
    )

    assert stored.checkpoint_serialization == "{not-json}"


def test_record_defines_no_storage_behavior() -> None:
    public_names = {
        name
        for name in vars(StoredState)
        if not name.startswith("_")
    }

    assert public_names == {
        field.name
        for field in fields(StoredState)
    }
