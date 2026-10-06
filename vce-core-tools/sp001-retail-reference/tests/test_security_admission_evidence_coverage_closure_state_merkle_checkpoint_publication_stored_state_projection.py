import inspect
import json

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state
)

UINT64_MAX = (1 << 64) - 1


def test_projection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(project)

    assert tuple(signature.parameters) == ("state",)
    assert (
        signature.parameters["state"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_projection_returns_nominal_stored_state() -> None:
    stored = project(state=create_state())

    assert isinstance(stored, StoredState)


def test_projection_preserves_complete_primitive_graph() -> None:
    state = create_state(
        publication_id="tenant://mx/publication-007",
        scalar=7,
        phase=Phase.COMMIT_DECIDED,
        revision=19,
    )
    intent = state.publication_intent
    envelope = intent.checkpoint_signature
    identity = envelope.signing_key_identity

    stored = project(state=state)

    assert stored.storage_schema_version == (
        SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION
    )
    assert stored.publication_id == intent.publication_id
    assert stored.checkpoint_serialization == (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=envelope.checkpoint,
        )
    )
    assert stored.signing_key_id == identity.key_id
    assert stored.signing_algorithm == identity.algorithm
    assert stored.public_key_encoding == (
        identity.public_key_encoding
    )
    assert stored.public_key_fingerprint == (
        identity.public_key_fingerprint
    )
    assert stored.signature_encoding == (
        envelope.signature_encoding
    )
    assert stored.signature is envelope.signature
    assert stored.phase == state.phase.value
    assert stored.revision == state.revision


@pytest.mark.parametrize("phase", tuple(Phase))
def test_projection_preserves_every_phase(
    phase: Phase,
) -> None:
    state = create_state(
        phase=phase,
    )

    stored = project(state=state)

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
def test_projection_preserves_portable_revision(
    revision: int,
) -> None:
    state = create_state(
        revision=revision,
    )

    stored = project(state=state)

    assert stored.revision == revision
    assert type(stored.revision) is int


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "tenant://mx/publication-007",
        "urn:sp001:publication:0001",
        "opaque identifier",
    ),
)
def test_projection_preserves_opaque_publication_id(
    publication_id: str,
) -> None:
    state = create_state(
        publication_id=publication_id,
    )

    stored = project(state=state)

    assert stored.publication_id == publication_id


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
def test_projection_preserves_exact_signature_bytes(
    scalar: int,
) -> None:
    state = create_state(
        scalar=scalar,
    )
    signature = (
        state
        .publication_intent
        .checkpoint_signature
        .signature
    )

    stored = project(state=state)

    assert stored.signature is signature
    assert stored.signature == signature


def test_projection_uses_canonical_checkpoint_json() -> None:
    state = create_state()
    checkpoint = (
        state
        .publication_intent
        .checkpoint_signature
        .checkpoint
    )

    stored = project(state=state)

    assert stored.checkpoint_serialization == (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )
    assert stored.checkpoint_serialization.startswith(
        '{"domain":'
    )
    assert " " not in stored.checkpoint_serialization


def test_projected_checkpoint_json_has_exact_keys() -> None:
    stored = project(state=create_state())
    decoded = json.loads(
        stored.checkpoint_serialization
    )

    assert tuple(decoded) == (
        "domain",
        "origin",
        "root",
    )
    assert tuple(decoded["root"]) == (
        "algorithm",
        "leaf_count",
        "tree_hash_profile",
        "value",
    )


def test_projection_is_deterministic_for_same_state() -> None:
    state = create_state()

    assert project(state=state) == project(state=state)


def test_projection_does_not_mutate_source_state() -> None:
    state = create_state(
        phase=Phase.PREPARED,
        revision=2,
    )
    intent = state.publication_intent
    envelope = intent.checkpoint_signature
    signature = envelope.signature

    project(state=state)

    assert state.publication_intent is intent
    assert intent.checkpoint_signature is envelope
    assert envelope.signature is signature
    assert state.phase is Phase.PREPARED
    assert state.revision == 2


@pytest.mark.parametrize(
    "invalid_state",
    (
        None,
        object(),
        "state",
        1,
        (),
    ),
)
def test_projection_rejects_invalid_nominal_state(
    invalid_state: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState"
        ),
    ):
        project(state=invalid_state)


def test_projection_does_not_encode_signature_as_text() -> None:
    stored = project(state=create_state())

    assert type(stored.signature) is bytes


def test_projection_defines_no_storage_capability() -> None:
    source = inspect.getsource(project).lower()

    for forbidden_term in (
        "sqlite",
        "open(",
        "write(",
        "commit(",
        "rollback(",
        "pickle",
        "base64",
    ):
        assert forbidden_term not in source
