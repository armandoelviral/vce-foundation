import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
)
StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)


def test_projection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(project)

    assert tuple(signature.parameters) == (
        "publication_intent",
    )
    assert (
        signature.parameters[
            "publication_intent"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_projection_returns_nominal_stored_intent() -> None:
    stored_intent = project(
        publication_intent=create_intent(),
    )

    assert isinstance(
        stored_intent,
        StoredIntent,
    )


def test_projection_preserves_complete_primitive_graph() -> None:
    intent = create_intent()
    signature = intent.checkpoint_signature
    identity = signature.signing_key_identity

    stored_intent = project(
        publication_intent=intent,
    )

    assert stored_intent.storage_schema_version == 1
    assert (
        stored_intent.publication_id
        == intent.publication_id
    )
    assert (
        stored_intent.checkpoint_serialization
        == serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=signature.checkpoint,
        )
    )
    assert (
        stored_intent.signing_key_id
        == identity.key_id
    )
    assert (
        stored_intent.signing_algorithm
        == identity.algorithm
    )
    assert (
        stored_intent.public_key_encoding
        == identity.public_key_encoding
    )
    assert (
        stored_intent.public_key_fingerprint
        == identity.public_key_fingerprint
    )
    assert (
        stored_intent.signature_encoding
        == signature.signature_encoding
    )
    assert (
        stored_intent.signature
        == signature.signature
    )


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "urn:publication:regional:001",
        "tenant/a/checkpoint/0007",
        " publicación ",
    ),
)
def test_projection_preserves_opaque_publication_id(
    publication_id: str,
) -> None:
    intent = create_intent(
        publication_id=publication_id,
    )

    stored_intent = project(
        publication_intent=intent,
    )

    assert (
        stored_intent.publication_id
        == publication_id
    )


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        3,
        7,
        19,
        65537,
    ),
)
def test_projection_preserves_exact_signature_bytes(
    scalar: int,
) -> None:
    intent = create_intent(
        scalar=scalar,
    )

    stored_intent = project(
        publication_intent=intent,
    )

    assert (
        stored_intent.signature
        is intent.checkpoint_signature.signature
    )


def test_projection_uses_canonical_checkpoint_json() -> None:
    intent = create_intent()

    serialization = project(
        publication_intent=intent,
    ).checkpoint_serialization

    assert serialization == json.dumps(
        json.loads(serialization),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_projected_checkpoint_json_has_exact_keys() -> None:
    intent = create_intent()

    document = json.loads(
        project(
            publication_intent=intent,
        ).checkpoint_serialization
    )

    assert set(document) == {
        "domain",
        "origin",
        "root",
    }
    assert set(document["root"]) == {
        "algorithm",
        "leaf_count",
        "tree_hash_profile",
        "value",
    }


def test_projection_is_deterministic_for_same_intent() -> None:
    intent = create_intent()

    first = project(
        publication_intent=intent,
    )
    second = project(
        publication_intent=intent,
    )

    assert first == second


def test_projection_does_not_mutate_source_intent() -> None:
    intent = create_intent()
    original_signature = (
        intent.checkpoint_signature
    )

    project(
        publication_intent=intent,
    )

    assert (
        intent.checkpoint_signature
        is original_signature
    )


@pytest.mark.parametrize(
    "invalid_intent",
    (
        None,
        object(),
        "intent",
        (),
        1,
        True,
    ),
)
def test_projection_rejects_invalid_nominal_intent(
    invalid_intent: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        project(
            publication_intent=invalid_intent,
        )


def test_projection_does_not_encode_signature_as_text() -> None:
    stored_intent = project(
        publication_intent=create_intent(),
    )

    assert type(stored_intent.signature) is bytes


def test_projection_defines_no_storage_or_signing_capability() -> None:
    source = inspect.getsource(project)

    assert "sqlite" not in source
    assert ".sign(" not in source
    assert "private_key" not in source
    assert "open(" not in source
