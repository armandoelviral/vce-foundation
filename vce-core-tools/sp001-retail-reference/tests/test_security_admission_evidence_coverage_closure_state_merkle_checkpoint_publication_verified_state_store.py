from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_verified_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
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


def create_verified_store(
    tmp_path,
    *,
    binding_set_size: int = 3,
):
    durable_store = create_store(tmp_path)

    verified_store = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore(
            state_store=durable_store,
            binding_set=create_binding_set(
                size=binding_set_size,
            ),
        )
    )

    return durable_store, verified_store


def state_for_key_index(
    index: int,
):
    state = create_state(
        publication_id=f"publication-{index:03d}",
    )
    _, checkpoint_signature = signed_checkpoint(
        scalar=index,
        key_id=(
            f"kms://security-admission/"
            f"key-{index:03d}"
        ),
    )
    publication_intent = replace(
        state.publication_intent,
        checkpoint_signature=checkpoint_signature,
    )

    return replace(
        state,
        publication_intent=publication_intent,
    )


def tampered_state(
    state,
):
    checkpoint_signature = (
        state
        .publication_intent
        .checkpoint_signature
    )
    signature = checkpoint_signature.signature
    changed_signature = (
        signature[:-1]
        + bytes((signature[-1] ^ 1,))
    )
    changed_checkpoint_signature = replace(
        checkpoint_signature,
        signature=changed_signature,
    )
    changed_intent = replace(
        state.publication_intent,
        checkpoint_signature=changed_checkpoint_signature,
    )

    return replace(
        state,
        publication_intent=changed_intent,
    )


def prepared_successor(
    state,
):
    return replace(
        state,
        phase=(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase.PREPARED
        ),
        revision=state.revision + 1,
    )


def test_verified_store_implements_state_store_protocol(
    tmp_path,
) -> None:
    _, verified_store = create_verified_store(tmp_path)

    assert isinstance(
        verified_store,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
    )


def test_missing_state_remains_absent(
    tmp_path,
) -> None:
    _, verified_store = create_verified_store(tmp_path)

    assert (
        verified_store.read(
            publication_id="missing-publication",
        )
        is None
    )


def test_verified_create_and_read_round_trip(
    tmp_path,
) -> None:
    state = create_state()
    _, verified_store = create_verified_store(tmp_path)

    assert verified_store.create(state=state) is True
    assert (
        verified_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        == state
    )


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        3,
    ),
)
def test_each_provisioned_key_is_accepted(
    tmp_path,
    scalar: int,
) -> None:
    state = state_for_key_index(scalar)
    _, verified_store = create_verified_store(tmp_path)

    assert verified_store.create(state=state) is True
    assert (
        verified_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        == state
    )


def test_unprovisioned_key_is_rejected_before_create(
    tmp_path,
) -> None:
    state = create_state(
        scalar=4,
    )
    durable_store, verified_store = create_verified_store(
        tmp_path,
        binding_set_size=3,
    )

    with pytest.raises(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
        match="signature verification failed",
    ):
        verified_store.create(state=state)

    assert (
        durable_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        is None
    )


def test_tampered_signature_is_rejected_before_create(
    tmp_path,
) -> None:
    state = tampered_state(create_state())
    durable_store, verified_store = create_verified_store(
        tmp_path,
    )

    with pytest.raises(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
    ):
        verified_store.create(state=state)

    assert (
        durable_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        is None
    )


def test_tampered_durable_state_fails_closed_on_read(
    tmp_path,
) -> None:
    state = tampered_state(create_state())
    durable_store, verified_store = create_verified_store(
        tmp_path,
    )

    assert durable_store.create(state=state) is True

    with pytest.raises(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
    ):
        verified_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )


def test_valid_compare_and_swap_is_preserved(
    tmp_path,
) -> None:
    state = create_state()
    successor = prepared_successor(state)
    _, verified_store = create_verified_store(tmp_path)

    assert verified_store.create(state=state) is True
    assert (
        verified_store.compare_and_swap(
            expected_revision=state.revision,
            next_state=successor,
        )
        is True
    )
    assert (
        verified_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        == successor
    )


def test_stale_compare_and_swap_result_is_preserved(
    tmp_path,
) -> None:
    state = create_state()
    successor = replace(
        prepared_successor(state),
        revision=state.revision + 2,
    )
    _, verified_store = create_verified_store(tmp_path)

    assert verified_store.create(state=state) is True
    assert (
        verified_store.compare_and_swap(
            expected_revision=state.revision + 1,
            next_state=successor,
        )
        is False
    )
    assert (
        verified_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        == state
    )


def test_tampered_successor_is_rejected_before_compare_and_swap(
    tmp_path,
) -> None:
    state = create_state()
    successor = tampered_state(
        prepared_successor(state)
    )
    durable_store, verified_store = create_verified_store(
        tmp_path,
    )

    assert verified_store.create(state=state) is True

    with pytest.raises(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
    ):
        verified_store.compare_and_swap(
            expected_revision=state.revision,
            next_state=successor,
        )

    assert (
        durable_store.read(
            publication_id=(
                state.publication_intent.publication_id
            ),
        )
        == state
    )


def test_invalid_state_store_is_rejected() -> None:
    with pytest.raises(
        TypeError,
        match="state_store",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore(
            state_store=object(),
            binding_set=create_binding_set(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        [],
        {},
        "binding-set",
        b"binding-set",
        1,
        True,
    ),
)
def test_invalid_binding_set_is_rejected(
    tmp_path,
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="binding_set",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore(
            state_store=create_store(tmp_path),
            binding_set=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        "state",
        b"state",
        1,
        True,
    ),
)
def test_create_rejects_invalid_state(
    tmp_path,
    value: object,
) -> None:
    _, verified_store = create_verified_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="state",
    ):
        verified_store.create(state=value)


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        "state",
        b"state",
        1,
        True,
    ),
)
def test_compare_and_swap_rejects_invalid_state(
    tmp_path,
    value: object,
) -> None:
    _, verified_store = create_verified_store(tmp_path)

    with pytest.raises(
        TypeError,
        match="state",
    ):
        verified_store.compare_and_swap(
            expected_revision=1,
            next_state=value,
        )


def test_verification_error_is_nominal_runtime_error() -> None:
    assert issubclass(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError,
        RuntimeError,
    )


def test_verified_store_defines_no_sqlite_or_cryptographic_key_material() -> None:
    import inspect

    from sp001.services import (
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_verified_state_store,
    )

    source = inspect.getsource(
        security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_verified_state_store
    )

    assert "sqlite3" not in source
    assert "private_key" not in source
    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
