import inspect
from dataclasses import FrozenInstanceError
from dataclasses import fields
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    create_stored_state,
)


StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)


def create_stored_intent() -> StoredIntent:
    state = create_stored_state()

    return StoredIntent(
        storage_schema_version=(
            state.storage_schema_version
        ),
        publication_id=state.publication_id,
        checkpoint_serialization=(
            state.checkpoint_serialization
        ),
        signing_key_id=state.signing_key_id,
        signing_algorithm=state.signing_algorithm,
        public_key_encoding=(
            state.public_key_encoding
        ),
        public_key_fingerprint=(
            state.public_key_fingerprint
        ),
        signature_encoding=(
            state.signature_encoding
        ),
        signature=state.signature,
    )


def test_storage_schema_version_constant_is_exact() -> None:
    assert (
        create_stored_intent()
        .storage_schema_version
        == 1
    )


def test_stored_intent_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(StoredIntent)
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
    )


def test_stored_intent_preserves_exact_values() -> None:
    state = create_stored_state()
    intent = create_stored_intent()

    assert intent.storage_schema_version == 1
    assert (
        intent.publication_id
        == state.publication_id
    )
    assert (
        intent.checkpoint_serialization
        == state.checkpoint_serialization
    )
    assert (
        intent.signing_key_id
        == state.signing_key_id
    )
    assert (
        intent.signing_algorithm
        == state.signing_algorithm
    )
    assert (
        intent.public_key_encoding
        == state.public_key_encoding
    )
    assert (
        intent.public_key_fingerprint
        == state.public_key_fingerprint
    )
    assert (
        intent.signature_encoding
        == state.signature_encoding
    )
    assert intent.signature == state.signature


@pytest.mark.parametrize(
    (
        "attribute",
        "value",
    ),
    (
        (
            "publication_id",
            "changed-publication",
        ),
        (
            "signature",
            b"changed-signature",
        ),
    ),
)
def test_stored_intent_is_frozen(
    attribute: str,
    value: object,
) -> None:
    intent = create_stored_intent()

    with pytest.raises(FrozenInstanceError):
        setattr(
            intent,
            attribute,
            value,
        )


def test_stored_intent_uses_slots() -> None:
    intent = create_stored_intent()

    assert not hasattr(intent, "__dict__")


def test_equal_primitive_values_are_equal() -> None:
    assert (
        create_stored_intent()
        == create_stored_intent()
    )


def test_different_primitive_values_are_not_equal() -> None:
    original = create_stored_intent()
    changed = replace(
        original,
        publication_id="different-publication",
    )

    assert changed != original


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "1",
        1.0,
        True,
        b"1",
    ),
)
def test_storage_schema_version_requires_exact_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="storage_schema_version",
    ):
        replace(
            create_stored_intent(),
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
    ),
)
def test_storage_schema_version_requires_positive_uint64(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="storage_schema_version",
    ):
        replace(
            create_stored_intent(),
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        2,
        3,
        (1 << 64) - 1,
    ),
)
def test_unknown_storage_schema_version_fails_closed(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="not supported",
    ):
        replace(
            create_stored_intent(),
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
        b"value",
        1,
        True,
        (),
    ),
)
def test_text_fields_require_exact_string(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=field_name,
    ):
        replace(
            create_stored_intent(),
            **{
                field_name: value,
            },
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
        match=field_name,
    ):
        replace(
            create_stored_intent(),
            **{
                field_name: "",
            },
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        b"0" * 64,
        1,
        True,
        (),
    ),
)
def test_public_key_fingerprint_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="public_key_fingerprint",
    ):
        replace(
            create_stored_intent(),
            public_key_fingerprint=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        "0" * 63,
        "0" * 65,
        "G" * 64,
        "A" * 64,
        "é" * 64,
    ),
)
def test_public_key_fingerprint_requires_lower_hex_sha256(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="64 lowercase hexadecimal",
    ):
        replace(
            create_stored_intent(),
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
        True,
        (),
    ),
)
def test_signature_requires_exact_bytes(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="signature",
    ):
        replace(
            create_stored_intent(),
            signature=value,
        )


def test_signature_rejects_empty_bytes() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        replace(
            create_stored_intent(),
            signature=b"",
        )


def test_record_does_not_parse_or_execute_checkpoint() -> None:
    source = inspect.getsource(StoredIntent)

    assert "json.loads" not in source
    assert "eval(" not in source
    assert "exec(" not in source


def test_record_defines_no_storage_behavior() -> None:
    assert not hasattr(StoredIntent, "read")
    assert not hasattr(StoredIntent, "create")
    assert not hasattr(StoredIntent, "write")
    assert not hasattr(StoredIntent, "delete")
