from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_durable_participant import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDurableParticipant,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_verified_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_sqlite_state_store import (
    create_store,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    signed_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    create_binding_set,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
Participant = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDurableParticipant
)
ParticipantStateError = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError
)
VerifiedStateStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore
)


def create_verified_store(
    tmp_path,
):
    durable_store = create_store(tmp_path)
    verified_store = VerifiedStateStore(
        state_store=durable_store,
        binding_set=create_binding_set(),
    )

    return durable_store, verified_store


def create_participant(
    tmp_path,
    *,
    participant_id: str = "participant-001",
):
    durable_store, verified_store = (
        create_verified_store(tmp_path)
    )
    participant = Participant(
        participant_id=participant_id,
        state_store=verified_store,
    )

    return durable_store, verified_store, participant


def different_valid_intent(
    *,
    publication_id: str,
):
    state = create_state(
        publication_id=publication_id,
    )
    _, checkpoint_signature = signed_checkpoint(
        scalar=1,
        key_id="kms://security-admission/key-001",
        origin="different-origin",
    )

    return replace(
        state.publication_intent,
        checkpoint_signature=checkpoint_signature,
    )


def test_durable_participant_implements_protocol(
    tmp_path,
) -> None:
    _, _, participant = create_participant(
        tmp_path
    )

    assert isinstance(
        participant,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
    )


def test_participant_identity_is_preserved(
    tmp_path,
) -> None:
    _, _, participant = create_participant(
        tmp_path,
        participant_id="node://region-a/001",
    )

    assert (
        participant.participant_id
        == "node://region-a/001"
    )


def test_prepare_creates_and_durably_prepares_state(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )

    prepared = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    assert prepared.phase is Phase.PREPARED
    assert prepared.revision == 2
    assert (
        prepared.publication_intent
        is state.publication_intent
    )
    assert (
        verified_store.read(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )
        == prepared
    )


def test_prepare_is_idempotent(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )

    first = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    second = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    assert second == first
    assert second.revision == 2


def test_concurrent_prepare_calls_converge(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )

    with ThreadPoolExecutor(
        max_workers=2,
    ) as executor:
        futures = tuple(
            executor.submit(
                participant.prepare,
                publication_intent=(
                    state.publication_intent
                ),
            )
            for _ in range(2)
        )

    results = tuple(
        future.result()
        for future in futures
    )

    assert tuple(
        result.phase
        for result in results
    ) == (
        Phase.PREPARED,
        Phase.PREPARED,
    )
    assert tuple(
        result.revision
        for result in results
    ) == (
        2,
        2,
    )


def test_same_identifier_cannot_replace_intent(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )

    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    with pytest.raises(
        ParticipantStateError,
        match="different publication intent",
    ):
        participant.prepare(
            publication_intent=(
                different_valid_intent(
                    publication_id=(
                        state
                        .publication_intent
                        .publication_id
                    ),
                )
            ),
        )


def test_commit_reaches_terminal_committed_state(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    prepared = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    committed = participant.commit(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    assert prepared.revision == 2
    assert committed.phase is Phase.COMMITTED
    assert committed.revision == 4
    assert (
        verified_store.read(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )
        == committed
    )


def test_commit_is_idempotent(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    first = participant.commit(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )
    second = participant.commit(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    assert second == first
    assert second.phase is Phase.COMMITTED
    assert second.revision == 4


def test_duplicate_prepare_after_commit_returns_committed_state(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    committed = participant.commit(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    result = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    assert result == committed


def test_commit_requires_existing_state(
    tmp_path,
) -> None:
    _, _, participant = create_participant(
        tmp_path
    )

    with pytest.raises(
        ParticipantStateError,
        match="does not exist",
    ):
        participant.commit(
            publication_id="missing",
        )


def test_commit_requires_prepared_state(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    assert verified_store.create(
        state=state,
    )

    with pytest.raises(
        ParticipantStateError,
        match="cannot be committed",
    ):
        participant.commit(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )


def test_abort_from_prepared_reaches_terminal_aborted_state(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )

    aborted = participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    assert aborted.phase is Phase.ABORTED
    assert aborted.revision == 4
    assert (
        verified_store.read(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )
        == aborted
    )


def test_abort_from_recorded_intent_reaches_aborted_state(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    assert verified_store.create(
        state=state,
    )

    aborted = participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    assert aborted.phase is Phase.ABORTED
    assert aborted.revision == 3


def test_abort_is_idempotent(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    assert verified_store.create(
        state=state,
    )

    first = participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )
    second = participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    assert second == first
    assert second.phase is Phase.ABORTED


def test_aborted_publication_cannot_be_prepared(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    with pytest.raises(
        ParticipantStateError,
        match="cannot be prepared",
    ):
        participant.prepare(
            publication_intent=(
                state.publication_intent
            ),
        )


def test_aborted_publication_cannot_be_committed(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    participant.abort(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    with pytest.raises(
        ParticipantStateError,
        match="cannot be committed",
    ):
        participant.commit(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )


def test_commit_decision_cannot_be_aborted(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store, participant = (
        create_participant(tmp_path)
    )
    prepared = participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    commit_decided = replace(
        prepared,
        phase=Phase.COMMIT_DECIDED,
        revision=3,
    )
    assert verified_store.compare_and_swap(
        expected_revision=2,
        next_state=commit_decided,
    )

    with pytest.raises(
        ParticipantStateError,
        match="cannot be aborted",
    ):
        participant.abort(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )


def test_committed_publication_cannot_be_aborted(
    tmp_path,
) -> None:
    state = create_state()
    _, _, participant = create_participant(
        tmp_path
    )
    participant.prepare(
        publication_intent=(
            state.publication_intent
        ),
    )
    participant.commit(
        publication_id=(
            state
            .publication_intent
            .publication_id
        ),
    )

    with pytest.raises(
        ParticipantStateError,
        match="cannot be aborted",
    ):
        participant.abort(
            publication_id=(
                state
                .publication_intent
                .publication_id
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        "intent",
        b"intent",
        1,
        True,
    ),
)
def test_prepare_rejects_invalid_intent(
    tmp_path,
    value: object,
) -> None:
    _, _, participant = create_participant(
        tmp_path
    )

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        participant.prepare(
            publication_intent=value,
        )


@pytest.mark.parametrize(
    "method_name",
    (
        "commit",
        "abort",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        b"publication",
        1,
        True,
    ),
)
def test_decision_methods_reject_invalid_identifier_type(
    tmp_path,
    method_name: str,
    value: object,
) -> None:
    _, _, participant = create_participant(
        tmp_path
    )

    with pytest.raises(
        TypeError,
        match="publication_id",
    ):
        getattr(
            participant,
            method_name,
        )(
            publication_id=value,
        )


@pytest.mark.parametrize(
    "method_name",
    (
        "commit",
        "abort",
    ),
)
def test_decision_methods_reject_empty_identifier(
    tmp_path,
    method_name: str,
) -> None:
    _, _, participant = create_participant(
        tmp_path
    )

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        getattr(
            participant,
            method_name,
        )(
            publication_id="",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        b"participant",
        1,
        True,
    ),
)
def test_constructor_rejects_invalid_participant_identifier_type(
    tmp_path,
    value: object,
) -> None:
    _, verified_store = create_verified_store(
        tmp_path
    )

    with pytest.raises(
        TypeError,
        match="participant_id",
    ):
        Participant(
            participant_id=value,
            state_store=verified_store,
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        " ",
        "\t",
        "\n",
    ),
)
def test_constructor_rejects_blank_participant_identifier(
    tmp_path,
    value: str,
) -> None:
    _, verified_store = create_verified_store(
        tmp_path
    )

    with pytest.raises(
        ValueError,
        match="must not be blank",
    ):
        Participant(
            participant_id=value,
            state_store=verified_store,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        "store",
        1,
        True,
    ),
)
def test_constructor_requires_verified_state_store(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="state_store",
    ):
        Participant(
            participant_id="participant-001",
            state_store=value,
        )


def test_raw_sqlite_store_is_rejected(
    tmp_path,
) -> None:
    with pytest.raises(
        TypeError,
        match="state_store",
    ):
        Participant(
            participant_id="participant-001",
            state_store=create_store(tmp_path),
        )


class AlwaysConflictingStore(
    VerifiedStateStore
):
    def __init__(
        self,
        *,
        state,
    ) -> None:
        self.state = state
        self.compare_and_swap_calls = 0

    def read(
        self,
        *,
        publication_id,
    ):
        return self.state

    def create(
        self,
        *,
        state,
    ):
        return False

    def compare_and_swap(
        self,
        *,
        expected_revision,
        next_state,
    ):
        self.compare_and_swap_calls += 1
        return False


def test_compare_and_swap_conflicts_are_bounded() -> None:
    state = create_state()
    store = AlwaysConflictingStore(
        state=state,
    )
    participant = Participant(
        participant_id="participant-001",
        state_store=store,
    )

    with pytest.raises(
        ParticipantStateError,
        match="bounded CAS attempts",
    ):
        participant.prepare(
            publication_intent=(
                state.publication_intent
            ),
        )

    assert store.compare_and_swap_calls == 4


class AlwaysLosingCreateStore(
    VerifiedStateStore
):
    def __init__(self) -> None:
        self.create_calls = 0

    def read(
        self,
        *,
        publication_id,
    ):
        return None

    def create(
        self,
        *,
        state,
    ):
        self.create_calls += 1
        return False

    def compare_and_swap(
        self,
        *,
        expected_revision,
        next_state,
    ):
        raise AssertionError(
            "compare_and_swap must not be called"
        )


def test_create_conflicts_are_bounded() -> None:
    state = create_state()
    store = AlwaysLosingCreateStore()
    participant = Participant(
        participant_id="participant-001",
        state_store=store,
    )

    with pytest.raises(
        ParticipantStateError,
        match="bounded CAS attempts",
    ):
        participant.prepare(
            publication_intent=(
                state.publication_intent
            ),
        )

    assert store.create_calls == 4


def test_state_error_is_nominal_runtime_error() -> None:
    assert issubclass(
        ParticipantStateError,
        RuntimeError,
    )


def test_participant_defines_no_transport_or_coordinator() -> None:
    import inspect

    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_durable_participant,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_durable_participant
    ).lower()

    for forbidden in (
        "socket",
        "http",
        "grpc",
        "requests",
        "coordinator",
        "quorum",
        "private_key",
        "pickle",
        "eval(",
        "exec(",
    ):
        assert forbidden not in source
