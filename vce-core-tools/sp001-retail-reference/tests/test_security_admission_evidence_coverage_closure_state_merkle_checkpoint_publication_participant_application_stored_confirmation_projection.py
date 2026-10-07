import inspect

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
project = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation
)


def test_projection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        project
    )

    assert tuple(signature.parameters) == (
        "confirmation",
    )
    assert (
        signature.parameters["confirmation"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        signature.parameters["confirmation"].annotation
        is Confirmation
    )
    assert (
        signature.return_annotation
        is StoredConfirmation
    )


def test_projection_returns_nominal_stored_confirmation() -> None:
    projected = project(
        confirmation=confirmation(),
    )

    assert isinstance(
        projected,
        StoredConfirmation,
    )


def test_projection_uses_supported_schema_version() -> None:
    projected = project(
        confirmation=confirmation(),
    )

    assert projected.storage_schema_version == 1


def test_projection_preserves_participant_identifier() -> None:
    projected = project(
        confirmation=confirmation(
            participant_id="participant/opaque",
        ),
    )

    assert (
        projected.participant_id
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
def test_projection_preserves_decision_and_terminal_phase(
    decision: Decision,
    phase: Phase,
) -> None:
    source = confirmation(
        decision=decision,
        publication_state=terminal_state(
            phase=phase,
        ),
    )

    projected = project(
        confirmation=source,
    )

    assert projected.decision == decision.value
    assert projected.publication_state.phase == phase.value


def test_projection_preserves_publication_identifier() -> None:
    projected = project(
        confirmation=confirmation(),
    )

    assert (
        projected.publication_state.publication_id
        == "publication-001"
    )


def test_projection_preserves_canonical_checkpoint() -> None:
    projected = project(
        confirmation=confirmation(),
    )

    assert (
        projected
        .publication_state
        .checkpoint_serialization
        .startswith("{")
    )
    assert (
        projected
        .publication_state
        .checkpoint_serialization
        .endswith("}")
    )


def test_projection_preserves_signing_identity() -> None:
    source = confirmation()

    projected = project(
        confirmation=source,
    )

    identity = (
        source
        .publication_state
        .publication_intent
        .checkpoint_signature
        .signing_key_identity
    )

    assert (
        projected.publication_state.signing_key_id
        == identity.key_id
    )
    assert (
        projected.publication_state.signing_algorithm
        == identity.algorithm
    )
    assert (
        projected.publication_state.public_key_encoding
        == identity.public_key_encoding
    )
    assert (
        projected
        .publication_state
        .public_key_fingerprint
        == identity.public_key_fingerprint
    )


def test_projection_preserves_exact_signature_bytes() -> None:
    source = confirmation()

    projected = project(
        confirmation=source,
    )

    assert (
        projected.publication_state.signature
        == (
            source
            .publication_state
            .publication_intent
            .checkpoint_signature
            .signature
        )
    )


@pytest.mark.parametrize(
    "revision",
    (
        1,
        4,
        2**32,
        2**64 - 1,
    ),
)
def test_projection_preserves_portable_revision(
    revision: int,
) -> None:
    source = confirmation(
        publication_state=terminal_state(
            revision=revision,
        ),
    )

    projected = project(
        confirmation=source,
    )

    assert (
        projected.publication_state.revision
        == revision
    )


def test_projection_is_deterministic_for_same_confirmation() -> None:
    source = confirmation()

    assert (
        project(
            confirmation=source,
        )
        == project(
            confirmation=source,
        )
    )


def test_projection_does_not_mutate_source() -> None:
    source = confirmation()
    before = repr(source)

    project(
        confirmation=source,
    )

    assert repr(source) == before


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "confirmation",
        object(),
    ),
)
def test_projection_rejects_invalid_nominal_confirmation(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="confirmation must be a",
    ):
        project(
            confirmation=value,
        )


def test_projection_defines_no_serialization_or_parsing() -> None:
    source = inspect.getsource(
        project
    ).lower()

    assert "json" not in source
    assert "serialize" not in source
    assert "parse" not in source


def test_projection_defines_no_storage_capability() -> None:
    source = inspect.getsource(
        project
    ).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_projection_defines_no_participant_effects() -> None:
    source = inspect.getsource(
        project
    )

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source
