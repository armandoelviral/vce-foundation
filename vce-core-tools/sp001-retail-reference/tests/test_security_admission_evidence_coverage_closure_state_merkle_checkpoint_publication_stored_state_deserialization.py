import inspect
import json
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
deserialize = (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state
)
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state
)

UINT64_MAX = (1 << 64) - 1


def create_stored_state(
    *,
    phase: Phase = Phase.INTENT_RECORDED,
    revision: int = 1,
    scalar: int = 1,
):
    return project(
        state=create_state(
            phase=phase,
            revision=revision,
            scalar=scalar,
        )
    )


def replace_checkpoint_data(
    stored,
    transform,
):
    data = json.loads(stored.checkpoint_serialization)
    transform(data)

    return replace(
        stored,
        checkpoint_serialization=json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=False,
        ),
    )


def test_deserializer_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(deserialize)

    assert tuple(signature.parameters) == (
        "stored_state",
    )
    assert (
        signature.parameters["stored_state"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_projection_deserialization_round_trip_is_exact() -> None:
    state = create_state(
        publication_id="publication-001",
        scalar=7,
        phase=Phase.COMMIT_DECIDED,
        revision=19,
    )
    stored = project(state=state)

    restored = deserialize(stored_state=stored)

    assert restored == state
    assert restored is not state


@pytest.mark.parametrize("phase", tuple(Phase))
def test_round_trip_preserves_every_phase(
    phase: Phase,
) -> None:
    state = create_state(
        phase=phase,
    )

    restored = deserialize(
        stored_state=project(state=state)
    )

    assert restored.phase is phase


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
def test_round_trip_preserves_portable_revision(
    revision: int,
) -> None:
    state = create_state(
        revision=revision,
    )

    restored = deserialize(
        stored_state=project(state=state)
    )

    assert restored.revision == revision


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        7,
        19,
        65537,
    ),
)
def test_round_trip_preserves_exact_signature(
    scalar: int,
) -> None:
    stored = create_stored_state(
        scalar=scalar,
    )

    restored = deserialize(
        stored_state=stored,
    )
    signature = (
        restored
        .publication_intent
        .checkpoint_signature
        .signature
    )

    assert signature is stored.signature
    assert signature == stored.signature


def test_round_trip_preserves_signing_identity() -> None:
    stored = create_stored_state()

    restored = deserialize(
        stored_state=stored,
    )
    identity = (
        restored
        .publication_intent
        .checkpoint_signature
        .signing_key_identity
    )

    assert identity.key_id == stored.signing_key_id
    assert identity.algorithm == stored.signing_algorithm
    assert identity.public_key_encoding == (
        stored.public_key_encoding
    )
    assert identity.public_key_fingerprint == (
        stored.public_key_fingerprint
    )


def test_round_trip_preserves_checkpoint_graph() -> None:
    stored = create_stored_state()

    restored = deserialize(
        stored_state=stored,
    )
    checkpoint = (
        restored
        .publication_intent
        .checkpoint_signature
        .checkpoint
    )
    root = checkpoint.root
    data = json.loads(
        stored.checkpoint_serialization
    )

    assert checkpoint.origin == data["origin"]
    assert root.algorithm == data["root"]["algorithm"]
    assert root.tree_hash_profile == (
        data["root"]["tree_hash_profile"]
    )
    assert root.leaf_count == data["root"]["leaf_count"]
    assert root.value == data["root"]["value"]


def test_deserialization_does_not_mutate_stored_state() -> None:
    stored = create_stored_state()
    serialization = stored.checkpoint_serialization
    signature = stored.signature

    deserialize(stored_state=stored)

    assert stored.checkpoint_serialization is serialization
    assert stored.signature is signature
    assert stored.phase == Phase.INTENT_RECORDED.value
    assert stored.revision == 1


@pytest.mark.parametrize(
    "invalid_stored_state",
    (
        None,
        object(),
        "stored-state",
        1,
        (),
    ),
)
def test_deserializer_requires_nominal_stored_state(
    invalid_stored_state: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "stored_state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationStoredState"
        ),
    ):
        deserialize(
            stored_state=invalid_stored_state,
        )


@pytest.mark.parametrize(
    "invalid_json",
    (
        "{",
        "not-json",
        '{"domain":',
        '{"domain":"value",}',
    ),
)
def test_malformed_checkpoint_json_fails_closed(
    invalid_json: str,
) -> None:
    stored = replace(
        create_stored_state(),
        checkpoint_serialization=invalid_json,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must contain "
            "valid JSON"
        ),
    ):
        deserialize(stored_state=stored)


@pytest.mark.parametrize(
    "json_value",
    (
        "[]",
        '"checkpoint"',
        "1",
        "true",
        "null",
    ),
)
def test_checkpoint_requires_json_object(
    json_value: str,
) -> None:
    stored = replace(
        create_stored_state(),
        checkpoint_serialization=json_value,
    )

    with pytest.raises(
        TypeError,
        match="checkpoint must be a JSON object",
    ):
        deserialize(stored_state=stored)


def test_checkpoint_rejects_missing_key() -> None:
    stored = create_stored_state()
    data = json.loads(
        stored.checkpoint_serialization
    )
    del data["domain"]
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            data,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint must contain exactly "
            "the required keys"
        ),
    ):
        deserialize(stored_state=changed)


def test_checkpoint_rejects_extra_key() -> None:
    stored = create_stored_state()

    changed = replace_checkpoint_data(
        stored,
        lambda data: data.update({"extra": "value"}),
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint must contain exactly "
            "the required keys"
        ),
    ):
        deserialize(stored_state=changed)


def test_checkpoint_rejects_wrong_domain() -> None:
    stored = create_stored_state()

    changed = replace_checkpoint_data(
        stored,
        lambda data: data.update(
            {"domain": "UNTRUSTED-DOMAIN"}
        ),
    )

    with pytest.raises(
        ValueError,
        match="checkpoint domain is not supported",
    ):
        deserialize(stored_state=changed)


@pytest.mark.parametrize(
    "root_value",
    (
        None,
        [],
        "root",
        1,
        True,
    ),
)
def test_root_requires_json_object(
    root_value: object,
) -> None:
    stored = create_stored_state()

    changed = replace_checkpoint_data(
        stored,
        lambda data: data.update(
            {"root": root_value}
        ),
    )

    with pytest.raises(
        TypeError,
        match=(
            "checkpoint root must be a JSON object"
        ),
    ):
        deserialize(stored_state=changed)


def test_root_rejects_missing_key() -> None:
    stored = create_stored_state()

    def remove_value(data: dict[str, object]) -> None:
        del data["root"]["value"]

    changed = replace_checkpoint_data(
        stored,
        remove_value,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint root must contain exactly "
            "the required keys"
        ),
    ):
        deserialize(stored_state=changed)


def test_root_rejects_extra_key() -> None:
    stored = create_stored_state()

    def add_extra(data: dict[str, object]) -> None:
        data["root"]["extra"] = "value"

    changed = replace_checkpoint_data(
        stored,
        add_extra,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint root must contain exactly "
            "the required keys"
        ),
    ):
        deserialize(stored_state=changed)


def test_duplicate_checkpoint_key_fails_closed() -> None:
    stored = create_stored_state()
    duplicate = stored.checkpoint_serialization.replace(
        '{"domain":',
        '{"domain":"duplicate","domain":',
        1,
    )
    changed = replace(
        stored,
        checkpoint_serialization=duplicate,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must not "
            "contain duplicate keys"
        ),
    ):
        deserialize(stored_state=changed)


def test_duplicate_root_key_fails_closed() -> None:
    stored = create_stored_state()
    duplicate = stored.checkpoint_serialization.replace(
        '"root":{"algorithm":',
        '"root":{"algorithm":"duplicate","algorithm":',
        1,
    )
    changed = replace(
        stored,
        checkpoint_serialization=duplicate,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must not "
            "contain duplicate keys"
        ),
    ):
        deserialize(stored_state=changed)


@pytest.mark.parametrize(
    "constant",
    (
        "NaN",
        "Infinity",
        "-Infinity",
    ),
)
def test_non_finite_json_number_fails_closed(
    constant: str,
) -> None:
    stored = create_stored_state()
    changed_serialization = (
        stored.checkpoint_serialization.replace(
            '"leaf_count":3',
            f'"leaf_count":{constant}',
            1,
        )
    )
    changed = replace(
        stored,
        checkpoint_serialization=changed_serialization,
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must not contain "
            "non-finite value"
        ),
    ):
        deserialize(stored_state=changed)


def test_whitespace_variant_is_rejected_as_noncanonical() -> None:
    stored = create_stored_state()
    changed = replace(
        stored,
        checkpoint_serialization=(
            stored.checkpoint_serialization.replace(
                ',"origin"',
                ', "origin"',
                1,
            )
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must be canonical"
        ),
    ):
        deserialize(stored_state=changed)


def test_key_order_variant_is_rejected_as_noncanonical() -> None:
    stored = create_stored_state()
    data = json.loads(
        stored.checkpoint_serialization
    )
    reordered = {
        "origin": data["origin"],
        "domain": data["domain"],
        "root": data["root"],
    }
    changed = replace(
        stored,
        checkpoint_serialization=json.dumps(
            reordered,
            separators=(",", ":"),
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "checkpoint_serialization must be canonical"
        ),
    ):
        deserialize(stored_state=changed)


@pytest.mark.parametrize(
    "field_name,value",
    (
        ("algorithm", "SHA-512"),
        ("tree_hash_profile", "UNKNOWN"),
        ("leaf_count", 0),
        ("leaf_count", -1),
        ("leaf_count", True),
        ("value", "0" * 63),
        ("value", "G" * 64),
    ),
)
def test_invalid_root_value_fails_nominal_reconstruction(
    field_name: str,
    value: object,
) -> None:
    stored = create_stored_state()

    def mutate(data: dict[str, object]) -> None:
        data["root"][field_name] = value

    changed = replace_checkpoint_data(
        stored,
        mutate,
    )

    with pytest.raises((TypeError, ValueError)):
        deserialize(stored_state=changed)


def test_deserializer_uses_no_executable_object_codec() -> None:
    source = inspect.getsource(deserialize).lower()

    for forbidden_term in (
        "pickle",
        "marshal",
        "eval(",
        "exec(",
        "yaml",
    ):
        assert forbidden_term not in source
