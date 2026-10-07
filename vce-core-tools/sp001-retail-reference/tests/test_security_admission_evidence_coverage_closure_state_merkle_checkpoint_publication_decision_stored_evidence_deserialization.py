import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence_projection import (
    zero_preparation_abort,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_commit,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    create_set,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)


def project_decision_record(
    decision_record,
) -> StoredEvidence:
    return (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            decision_record=decision_record,
        )
    )


def test_deserialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert tuple(signature.parameters) == (
        "stored_evidence",
        "participant_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_commit_round_trip_is_exact(
    size: int,
) -> None:
    original, _ = project_commit(
        size=size,
    )
    stored_evidence = project_decision_record(
        original,
    )

    rebuilt = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=original.participant_set,
        )
    )

    assert rebuilt == original
    assert rebuilt.decision is Decision.COMMIT


def test_zero_preparation_abort_round_trip_is_exact() -> None:
    original = zero_preparation_abort()
    stored_evidence = project_decision_record(
        original,
    )

    rebuilt = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=original.participant_set,
        )
    )

    assert rebuilt == original
    assert rebuilt.decision is Decision.ABORT
    assert rebuilt.preparation_set.preparations == ()


def test_zero_preparation_abort_retains_exact_signed_intent() -> None:
    original = zero_preparation_abort()
    stored_evidence = project_decision_record(
        original,
    )

    rebuilt = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=original.participant_set,
        )
    )

    assert (
        rebuilt.publication_intent
        == original.publication_intent
    )
    assert (
        rebuilt
        .publication_intent
        .checkpoint_signature
        .signature
        == (
            original
            .publication_intent
            .checkpoint_signature
            .signature
        )
    )


def test_rebuilt_record_uses_exact_provisioned_participant_set() -> None:
    original, _ = project_commit()
    stored_evidence = project_decision_record(
        original,
    )

    rebuilt = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=original.participant_set,
        )
    )

    assert (
        rebuilt.participant_set
        is original.participant_set
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "evidence",
        b"evidence",
        1,
        True,
        (),
    ),
)
def test_stored_evidence_rejects_invalid_type(
    value: object,
) -> None:
    original, _ = project_commit()

    with pytest.raises(
        TypeError,
        match="stored_evidence",
    ):
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=value,
            participant_set=original.participant_set,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "participants",
        b"participants",
        1,
        True,
        (),
    ),
)
def test_participant_set_rejects_invalid_type(
    value: object,
) -> None:
    original, _ = project_commit()
    stored_evidence = project_decision_record(
        original,
    )

    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=value,
        )


@pytest.mark.parametrize(
    "provisioned_size",
    (
        1,
        2,
        4,
        5,
    ),
)
def test_different_provisioned_roster_is_rejected(
    provisioned_size: int,
) -> None:
    original, _ = project_commit(
        size=3,
    )
    stored_evidence = project_decision_record(
        original,
    )

    with pytest.raises(
        ValueError,
        match="provisioned participant set",
    ):
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=stored_evidence,
            participant_set=create_set(
                size=provisioned_size,
            ),
        )


def test_changed_stored_decision_is_rejected() -> None:
    original, _ = project_commit()
    stored_evidence = project_decision_record(
        original,
    )
    changed_record = replace(
        stored_evidence.decision_record,
        decision=Decision.ABORT.value,
    )
    changed = StoredEvidence(
        publication_intent=(
            stored_evidence.publication_intent
        ),
        decision_record=changed_record,
    )

    with pytest.raises(
        ValueError,
        match="does not match the re-derived decision",
    ):
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=changed,
            participant_set=original.participant_set,
        )


def test_preparation_from_other_signed_intent_is_rejected() -> None:
    original, _ = project_commit()
    stored_evidence = project_decision_record(
        original,
    )
    other_intent = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=create_intent(
                scalar=2,
            ),
        )
    )

    participant_id, stored_state = (
        stored_evidence
        .decision_record
        .preparations[0]
    )
    changed_state = replace(
        stored_state,
        checkpoint_serialization=(
            other_intent.checkpoint_serialization
        ),
        signing_key_id=(
            other_intent.signing_key_id
        ),
        signing_algorithm=(
            other_intent.signing_algorithm
        ),
        public_key_encoding=(
            other_intent.public_key_encoding
        ),
        public_key_fingerprint=(
            other_intent.public_key_fingerprint
        ),
        signature_encoding=(
            other_intent.signature_encoding
        ),
        signature=other_intent.signature,
    )
    changed_record = replace(
        stored_evidence.decision_record,
        preparations=(
            (
                participant_id,
                changed_state,
            ),
            *(
                stored_evidence
                .decision_record
                .preparations[1:]
            ),
        ),
    )
    changed = StoredEvidence(
        publication_intent=(
            stored_evidence.publication_intent
        ),
        decision_record=changed_record,
    )

    with pytest.raises(
        ValueError,
        match="exact stored publication intent",
    ):
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
            stored_evidence=changed,
            participant_set=original.participant_set,
        )


def test_deserialization_defines_no_storage_behavior() -> None:
    source = inspect.getsource(
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "sqlite" not in source
    assert "open(" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_deserialization_defines_no_participant_effects() -> None:
    source = inspect.getsource(
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source


def test_deserialization_does_not_authenticate_signature() -> None:
    source = inspect.getsource(
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence
    )

    assert "verify_security_admission" not in source
