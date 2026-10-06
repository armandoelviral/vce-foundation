import inspect
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    signed_checkpoint,
)


def create_intent(
    *,
    publication_id: str = "publication-001",
    scalar: int = 1,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent:
    _, checkpoint_signature = signed_checkpoint(
        scalar=scalar,
    )

    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id=publication_id,
        checkpoint_signature=checkpoint_signature,
    )


def test_intent_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
        )
    ) == (
        "publication_id",
        "checkpoint_signature",
    )


def test_intent_preserves_exact_values() -> None:
    _, checkpoint_signature = signed_checkpoint()

    intent = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id="publication-001",
        checkpoint_signature=checkpoint_signature,
    )

    assert intent.publication_id == "publication-001"
    assert (
        intent.checkpoint_signature
        is checkpoint_signature
    )


@pytest.mark.parametrize(
    "publication_id",
    (
        "publication-001",
        "01J9Y6Q4X7M3K2P8R5T1V0WABC",
        "urn:sp001:publication:001",
        "region-a/store-042/checkpoint-007",
        "multicloud-ledger-entry-999",
    ),
)
def test_opaque_publication_identifiers_are_preserved(
    publication_id: str,
) -> None:
    intent = create_intent(
        publication_id=publication_id,
    )

    assert intent.publication_id == publication_id


def test_intent_is_frozen() -> None:
    intent = create_intent()

    with pytest.raises(FrozenInstanceError):
        intent.publication_id = "changed"


def test_intent_uses_slots() -> None:
    intent = create_intent()

    assert not hasattr(intent, "__dict__")


def test_equal_values_are_equal() -> None:
    _, checkpoint_signature = signed_checkpoint()

    first = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id="publication-001",
        checkpoint_signature=checkpoint_signature,
    )
    second = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id="publication-001",
        checkpoint_signature=checkpoint_signature,
    )

    assert first == second


def test_different_publication_identifiers_are_not_equal() -> None:
    _, checkpoint_signature = signed_checkpoint()

    first = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id="publication-001",
        checkpoint_signature=checkpoint_signature,
    )
    second = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
        publication_id="publication-002",
        checkpoint_signature=checkpoint_signature,
    )

    assert first != second


def test_different_checkpoint_signatures_are_not_equal() -> None:
    first = create_intent(
        scalar=1,
    )
    second = create_intent(
        scalar=2,
    )

    assert first != second


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"publication-001",
        1,
        True,
        (),
        object(),
    ),
)
def test_publication_id_rejects_invalid_type(
    value: object,
) -> None:
    _, checkpoint_signature = signed_checkpoint()

    with pytest.raises(
        TypeError,
        match="publication_id",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
            publication_id=value,
            checkpoint_signature=checkpoint_signature,
        )


def test_publication_id_rejects_empty_value() -> None:
    _, checkpoint_signature = signed_checkpoint()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
            publication_id="",
            checkpoint_signature=checkpoint_signature,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        "signature",
        b"signature",
        1,
        True,
        (),
        object(),
    ),
)
def test_checkpoint_signature_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="checkpoint_signature",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
            publication_id="publication-001",
            checkpoint_signature=value,
        )


def test_intent_defines_no_persistence_behavior() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
    ).lower()
    forbidden = (
        "sqlite",
        "database",
        "write_ahead",
        "commit",
        "rollback",
        "prepare",
        "publish(",
        "network",
    )

    assert all(
        token not in source
        for token in forbidden
    )


def test_intent_does_not_authorize_or_decide() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
    ).lower()
    forbidden = (
        "admission_decision",
        "authorization",
        "authority",
        "rejection",
        "classification",
    )

    assert all(
        token not in source
        for token in forbidden
    )
