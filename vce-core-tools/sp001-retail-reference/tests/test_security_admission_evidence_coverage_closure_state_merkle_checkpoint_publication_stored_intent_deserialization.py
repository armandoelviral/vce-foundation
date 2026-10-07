import inspect
import json
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


deserialize = (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
)
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent
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
def test_projected_intent_round_trips_exactly(
    scalar: int,
) -> None:
    original = create_intent(
        scalar=scalar,
    )
    stored = project(
        publication_intent=original,
    )

    rebuilt = deserialize(
        stored_intent=stored,
    )

    assert isinstance(
        rebuilt,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
    )
    assert rebuilt == original


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "urn:publication:regional:001",
        "tenant/a/checkpoint/0007",
        " publicación ",
    ),
)
def test_opaque_publication_id_round_trips(
    publication_id: str,
) -> None:
    original = create_intent(
        publication_id=publication_id,
    )

    rebuilt = deserialize(
        stored_intent=project(
            publication_intent=original,
        ),
    )

    assert rebuilt.publication_id == publication_id


def test_rebuilt_signature_retains_exact_bytes() -> None:
    original = create_intent()
    stored = project(
        publication_intent=original,
    )

    rebuilt = deserialize(
        stored_intent=stored,
    )

    assert (
        rebuilt.checkpoint_signature.signature
        is stored.signature
    )


def test_rebuilt_identity_retains_complete_graph() -> None:
    original = create_intent()
    stored = project(
        publication_intent=original,
    )

    rebuilt_identity = (
        deserialize(
            stored_intent=stored,
        )
        .checkpoint_signature
        .signing_key_identity
    )

    assert (
        rebuilt_identity.key_id
        == stored.signing_key_id
    )
    assert (
        rebuilt_identity.algorithm
        == stored.signing_algorithm
    )
    assert (
        rebuilt_identity.public_key_encoding
        == stored.public_key_encoding
    )
    assert (
        rebuilt_identity.public_key_fingerprint
        == stored.public_key_fingerprint
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "stored-intent",
        (),
        1,
        True,
    ),
)
def test_stored_intent_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_intent",
    ):
        deserialize(
            stored_intent=value,
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "{",
        "[",
        "not-json",
    ),
)
def test_invalid_checkpoint_json_is_rejected(
    serialization: str,
) -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    changed = replace(
        stored,
        checkpoint_serialization=serialization,
    )

    with pytest.raises(
        (TypeError, ValueError),
    ):
        deserialize(
            stored_intent=changed,
        )


def test_duplicate_checkpoint_keys_are_rejected() -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    changed_serialization = (
        stored.checkpoint_serialization.replace(
            '{"domain":',
            '{"domain":"duplicate","domain":',
            1,
        )
    )
    changed = replace(
        stored,
        checkpoint_serialization=changed_serialization,
    )

    with pytest.raises(
        ValueError,
        match="duplicate",
    ):
        deserialize(
            stored_intent=changed,
        )


@pytest.mark.parametrize(
    "constant",
    (
        "NaN",
        "Infinity",
        "-Infinity",
    ),
)
def test_nonfinite_json_constants_are_rejected(
    constant: str,
) -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    document["origin"] = float(
        constant.replace(
            "Infinity",
            "inf",
        ).replace(
            "NaN",
            "nan",
        )
    )
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            document,
            allow_nan=True,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match="non-finite",
    ):
        deserialize(
            stored_intent=changed,
        )


@pytest.mark.parametrize(
    "operation",
    (
        lambda value: value.pop("origin"),
        lambda value: value.update(
            unexpected=True,
        ),
    ),
)
def test_checkpoint_requires_exact_keys(
    operation,
) -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    operation(document)
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match="exact canonical keys",
    ):
        deserialize(
            stored_intent=changed,
        )


def test_checkpoint_requires_json_object() -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    changed = replace(
        stored,
        checkpoint_serialization="[]",
    )

    with pytest.raises(
        TypeError,
        match="JSON object",
    ):
        deserialize(
            stored_intent=changed,
        )


def test_unknown_checkpoint_domain_is_rejected() -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    document["domain"] = "OTHER-DOMAIN"
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match="domain",
    ):
        deserialize(
            stored_intent=changed,
        )


def test_checkpoint_root_requires_json_object() -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    document["root"] = None
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        TypeError,
        match="checkpoint root",
    ):
        deserialize(
            stored_intent=changed,
        )


@pytest.mark.parametrize(
    "operation",
    (
        lambda value: value.pop("value"),
        lambda value: value.update(
            unexpected=True,
        ),
    ),
)
def test_checkpoint_root_requires_exact_keys(
    operation,
) -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    operation(document["root"])
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match="exact canonical keys",
    ):
        deserialize(
            stored_intent=changed,
        )


def test_noncanonical_checkpoint_json_is_rejected() -> None:
    stored = project(
        publication_intent=create_intent(),
    )
    document = json.loads(
        stored.checkpoint_serialization
    )
    noncanonical = json.dumps(
        document,
        ensure_ascii=True,
        sort_keys=True,
    )
    assert (
        noncanonical
        != stored.checkpoint_serialization
    )
    changed = replace(
        stored,
        checkpoint_serialization=noncanonical,
    )

    with pytest.raises(
        ValueError,
        match="canonical",
    ):
        deserialize(
            stored_intent=changed,
        )


def test_deserialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(deserialize)

    assert tuple(signature.parameters) == (
        "stored_intent",
    )
    assert (
        signature.parameters[
            "stored_intent"
        ].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_deserialization_defines_no_storage_or_signing_effects() -> None:
    source = inspect.getsource(deserialize)

    assert "sqlite" not in source
    assert "open(" not in source
    assert ".sign(" not in source
    assert "private_key" not in source
