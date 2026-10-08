import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    confirmation,
    terminal_state,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
deserialize = (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)


def projected_confirmation(
    *,
    participant_id: str = "participant-001",
    decision: Decision = Decision.COMMIT,
    revision: int = 4,
    scalar: int = 1,
):
    phase = (
        Phase.COMMITTED
        if decision is Decision.COMMIT
        else Phase.ABORTED
    )
    original = confirmation(
        participant_id=participant_id,
        decision=decision,
        publication_state=terminal_state(
            phase=phase,
            revision=revision,
            scalar=scalar,
        ),
    )

    return (
        original,
        project(
            confirmation=original,
        ),
    )


def test_deserialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        deserialize
    )

    assert tuple(signature.parameters) == (
        "stored_confirmation",
    )
    assert (
        signature.parameters["stored_confirmation"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["stored_confirmation"].annotation
        is StoredConfirmation
    )
    assert (
        signature.return_annotation
        is Confirmation
    )


@pytest.mark.parametrize(
    "decision",
    (
        Decision.COMMIT,
        Decision.ABORT,
    ),
)
def test_round_trip_is_exact(
    decision: Decision,
) -> None:
    original, stored = projected_confirmation(
        decision=decision,
    )

    assert (
        deserialize(
            stored_confirmation=stored,
        )
        == original
    )


def test_deserialization_returns_nominal_confirmation() -> None:
    _, stored = projected_confirmation()

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert isinstance(
        rebuilt,
        Confirmation,
    )


def test_participant_identifier_is_preserved() -> None:
    _, stored = projected_confirmation(
        participant_id="participant/opaque",
    )

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert (
        rebuilt.participant_id
        == "participant/opaque"
    )


@pytest.mark.parametrize(
    ("decision", "phase"),
    (
        (
            Decision.COMMIT,
            Phase.COMMITTED,
        ),
        (
            Decision.ABORT,
            Phase.ABORTED,
        ),
    ),
)
def test_decision_and_terminal_phase_are_preserved(
    decision: Decision,
    phase: Phase,
) -> None:
    _, stored = projected_confirmation(
        decision=decision,
    )

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert rebuilt.decision is decision
    assert rebuilt.publication_state.phase is phase


@pytest.mark.parametrize(
    "revision",
    (
        1,
        4,
        2**32,
        2**64 - 1,
    ),
)
def test_revision_is_preserved(
    revision: int,
) -> None:
    _, stored = projected_confirmation(
        revision=revision,
    )

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert rebuilt.publication_state.revision == revision


def test_signed_publication_intent_is_reconstructed_exactly() -> None:
    original, stored = projected_confirmation(
        scalar=2,
    )

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert (
        rebuilt.publication_state.publication_intent
        == original.publication_state.publication_intent
    )


def test_signature_bytes_are_preserved_exactly() -> None:
    original, stored = projected_confirmation()

    rebuilt = deserialize(
        stored_confirmation=stored,
    )

    assert (
        rebuilt
        .publication_state
        .publication_intent
        .checkpoint_signature
        .signature
        == (
            original
            .publication_state
            .publication_intent
            .checkpoint_signature
            .signature
        )
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "stored-confirmation",
        object(),
    ),
)
def test_stored_confirmation_requires_nominal_type(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_confirmation must be a",
    ):
        deserialize(
            stored_confirmation=value,
        )


def test_unsupported_schema_version_fails_closed() -> None:
    _, stored = projected_confirmation()

    object.__setattr__(
        stored,
        "storage_schema_version",
        2,
    )

    with pytest.raises(
        ValueError,
        match="unsupported storage schema version",
    ):
        deserialize(
            stored_confirmation=stored,
        )


@pytest.mark.parametrize(
    "serialization",
    (
        "{",
        "[",
        "not-json",
    ),
)
def test_invalid_checkpoint_serialization_fails_closed(
    serialization: str,
) -> None:
    _, stored = projected_confirmation()
    changed_state = replace(
        stored.publication_state,
        checkpoint_serialization=serialization,
    )
    changed = replace(
        stored,
        publication_state=changed_state,
    )

    with pytest.raises(ValueError):
        deserialize(
            stored_confirmation=changed,
        )


def test_noncanonical_checkpoint_serialization_fails_closed() -> None:
    _, stored = projected_confirmation()
    changed_state = replace(
        stored.publication_state,
        checkpoint_serialization=(
            stored
            .publication_state
            .checkpoint_serialization
            + " "
        ),
    )
    changed = replace(
        stored,
        publication_state=changed_state,
    )

    with pytest.raises(
        ValueError,
        match="canonical",
    ):
        deserialize(
            stored_confirmation=changed,
        )


def test_changed_signature_fails_closed() -> None:
    _, stored = projected_confirmation()
    changed_state = replace(
        stored.publication_state,
        signature=b"invalid-signature",
    )
    changed = replace(
        stored,
        publication_state=changed_state,
    )

    with pytest.raises(ValueError):
        deserialize(
            stored_confirmation=changed,
        )


def test_deserialization_is_deterministic() -> None:
    _, stored = projected_confirmation()

    assert (
        deserialize(
            stored_confirmation=stored,
        )
        == deserialize(
            stored_confirmation=stored,
        )
    )


def test_deserialization_does_not_mutate_stored_value() -> None:
    _, stored = projected_confirmation()
    before = repr(stored)

    deserialize(
        stored_confirmation=stored,
    )

    assert repr(stored) == before


def test_deserialization_defines_no_storage_effects() -> None:
    source = inspect.getsource(
        deserialize
    ).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_deserialization_defines_no_participant_effects() -> None:
    source = inspect.getsource(
        deserialize
    )

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source


def test_deserialization_does_not_verify_signature() -> None:
    source = inspect.getsource(
        deserialize
    )

    assert "verify_security_admission" not in source
    assert "public_key" not in source


def test_deserialization_imports_no_unsafe_capability() -> None:
    module = inspect.getmodule(
        deserialize
    )
    assert module is not None

    source = inspect.getsource(module)

    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "__import__" not in source
