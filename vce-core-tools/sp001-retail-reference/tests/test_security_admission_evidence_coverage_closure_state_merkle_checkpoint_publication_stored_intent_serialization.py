import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-INTENT"
)


def stored_intent(
    *,
    publication_id: str = "publication-001",
    scalar: int = 1,
):
    return (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=create_intent(
                publication_id=publication_id,
                scalar=scalar,
            ),
        )
    )


def serialize(
    *,
    publication_id: str = "publication-001",
    scalar: int = 1,
) -> str:
    return (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored_intent(
                publication_id=publication_id,
                scalar=scalar,
            ),
        )
    )


def test_serialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
    )

    assert tuple(signature.parameters) == (
        "stored_intent",
    )
    assert (
        signature.parameters[
            "stored_intent"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert signature.return_annotation is str


def test_serialization_has_exact_top_level_keys() -> None:
    document = json.loads(serialize())

    assert set(document) == {
        "checkpoint_serialization",
        "domain",
        "public_key_encoding",
        "public_key_fingerprint",
        "publication_id",
        "signature_encoding",
        "signature_hex",
        "signing_algorithm",
        "signing_key_id",
        "storage_schema_version",
    }


def test_domain_is_exact() -> None:
    document = json.loads(serialize())

    assert document["domain"] == _DOMAIN


def test_complete_primitive_graph_is_preserved() -> None:
    stored = stored_intent()
    document = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored,
        )
    )

    assert document == {
        "checkpoint_serialization": (
            stored.checkpoint_serialization
        ),
        "domain": _DOMAIN,
        "public_key_encoding": (
            stored.public_key_encoding
        ),
        "public_key_fingerprint": (
            stored.public_key_fingerprint
        ),
        "publication_id": stored.publication_id,
        "signature_encoding": (
            stored.signature_encoding
        ),
        "signature_hex": stored.signature.hex(),
        "signing_algorithm": (
            stored.signing_algorithm
        ),
        "signing_key_id": stored.signing_key_id,
        "storage_schema_version": (
            stored.storage_schema_version
        ),
    }


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_exact_signature_bytes_are_hex_encoded(
    scalar: int,
) -> None:
    stored = stored_intent(
        scalar=scalar,
    )
    document = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored,
        )
    )

    assert (
        bytes.fromhex(document["signature_hex"])
        == stored.signature
    )


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "opaque/publication:value",
        "tenant:alpha:publication:42",
        "publicación-ñ",
    ),
)
def test_opaque_publication_identifier_is_preserved(
    publication_id: str,
) -> None:
    document = json.loads(
        serialize(
            publication_id=publication_id,
        )
    )

    assert (
        document["publication_id"]
        == publication_id
    )


def test_serialization_is_canonical_compact_json() -> None:
    serialization = serialize()
    document = json.loads(serialization)

    assert serialization == json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_serialization_is_deterministic() -> None:
    stored = stored_intent()

    first = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored,
        )
    )
    second = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=stored,
        )
    )

    assert first == second


def test_nested_checkpoint_remains_canonical_json_text() -> None:
    document = json.loads(serialize())
    checkpoint = document[
        "checkpoint_serialization"
    ]

    assert type(checkpoint) is str
    assert checkpoint == json.dumps(
        json.loads(checkpoint),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "intent",
        b"intent",
        1,
        True,
        (),
    ),
)
def test_invalid_stored_intent_is_rejected(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_intent",
    ):
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=value,
        )


def test_serialization_does_not_mutate_source() -> None:
    stored = stored_intent()
    before = stored

    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
        stored_intent=stored,
    )

    assert stored is before


def test_serialization_defines_no_storage_behavior() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert "write" not in source
    assert "read" not in source


def test_serialization_defines_no_signature_verification() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
    )

    assert "verify_security_admission" not in source
    assert "load_der_public_key" not in source
    assert "cryptography" not in source
