import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_binding_set_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    signed_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    create_binding_set,
)


def key_id(
    index: int,
) -> str:
    return (
        f"kms://security-admission/"
        f"key-{index:03d}"
    )


def signed_for_index(
    index: int,
):
    return signed_checkpoint(
        scalar=index,
        key_id=key_id(index),
    )[1]


@pytest.mark.parametrize(
    "index",
    (
        1,
        2,
        3,
        4,
        5,
    ),
)
def test_signature_resolves_and_verifies_from_set(
    index: int,
) -> None:
    signature = signed_for_index(index)
    binding_set = create_binding_set(
        size=5,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=signature,
            binding_set=binding_set,
        )
        is True
    )


def test_result_is_nominal_bool() -> None:
    signature = signed_for_index(1)

    result = (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=signature,
            binding_set=create_binding_set(),
        )
    )

    assert type(result) is bool


def test_unknown_identity_fails_closed() -> None:
    signature = signed_for_index(4)

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=signature,
            binding_set=create_binding_set(
                size=3,
            ),
        )
        is False
    )


def test_known_key_id_with_wrong_fingerprint_fails_closed() -> None:
    signature = signed_for_index(1)
    fingerprint = (
        signature
        .signing_key_identity
        .public_key_fingerprint
    )
    replacement = (
        "0" if fingerprint[0] != "0" else "1"
    )
    changed_identity = replace(
        signature.signing_key_identity,
        public_key_fingerprint=(
            replacement + fingerprint[1:]
        ),
    )
    changed = replace(
        signature,
        signing_key_identity=changed_identity,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=changed,
            binding_set=create_binding_set(),
        )
        is False
    )


def test_known_fingerprint_with_wrong_key_id_fails_closed() -> None:
    signature = signed_for_index(1)
    changed_identity = replace(
        signature.signing_key_identity,
        key_id="kms://security-admission/key-999",
    )
    changed = replace(
        signature,
        signing_key_identity=changed_identity,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=changed,
            binding_set=create_binding_set(),
        )
        is False
    )


def test_changed_checkpoint_fails_closed() -> None:
    signature = signed_for_index(1)
    changed = replace(
        signature,
        checkpoint=create_checkpoint(
            origin="different-origin",
        ),
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=changed,
            binding_set=create_binding_set(),
        )
        is False
    )


def test_signature_from_other_key_fails_closed() -> None:
    signature = signed_for_index(1)
    other = signed_for_index(2)
    changed = replace(
        signature,
        signature=other.signature,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=changed,
            binding_set=create_binding_set(),
        )
        is False
    )


def test_signature_for_other_payload_fails_closed() -> None:
    signature = signed_for_index(1)
    _, other = signed_checkpoint(
        scalar=1,
        key_id=key_id(1),
        origin="different-origin",
    )
    changed = replace(
        signature,
        signature=other.signature,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=changed,
            binding_set=create_binding_set(),
        )
        is False
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "signature",
        b"signature",
        1,
        True,
        (),
    ),
)
def test_checkpoint_signature_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="checkpoint_signature",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=value,
            binding_set=create_binding_set(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "binding-set",
        b"binding-set",
        1,
        True,
        (),
    ),
)
def test_binding_set_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="binding_set",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=signed_for_index(
                1
            ),
            binding_set=value,
        )


def test_verification_preserves_inputs() -> None:
    signature = signed_for_index(2)
    binding_set = create_binding_set()
    checkpoint = signature.checkpoint
    identity = signature.signing_key_identity
    signature_bytes = signature.signature
    bindings = binding_set.bindings

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
            checkpoint_signature=signature,
            binding_set=binding_set,
        )
        is True
    )

    assert signature.checkpoint is checkpoint
    assert signature.signing_key_identity is identity
    assert signature.signature is signature_bytes
    assert binding_set.bindings is bindings


def test_verification_has_exact_boundary() -> None:
    parameters = inspect.signature(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set
    ).parameters

    assert tuple(parameters) == (
        "checkpoint_signature",
        "binding_set",
    )


def test_verification_receives_no_private_key() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set
    )

    assert "private_key" not in source
    assert "private_bytes" not in source


def test_verification_does_not_authorize_or_decide() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set
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
