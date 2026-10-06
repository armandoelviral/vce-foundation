import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_binding_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    KEY_ID,
    signed_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    create_binding,
)


def test_exact_signature_and_binding_verify() -> None:
    _, signature = signed_checkpoint()
    binding = create_binding()

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
        is True
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
def test_multiple_matching_bindings_verify(
    scalar: int,
) -> None:
    _, signature = signed_checkpoint(
        scalar=scalar,
    )
    binding = create_binding(
        scalar=scalar,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
        is True
    )


def test_result_is_nominal_bool() -> None:
    _, signature = signed_checkpoint()
    binding = create_binding()

    result = (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
    )

    assert type(result) is bool


def test_wrong_public_key_binding_fails_closed() -> None:
    _, signature = signed_checkpoint(
        scalar=1,
    )
    binding = create_binding(
        scalar=2,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
        is False
    )


def test_wrong_key_id_binding_fails_closed() -> None:
    _, signature = signed_checkpoint(
        key_id=KEY_ID,
    )
    binding = create_binding(
        key_id="kms://security-admission/key-002",
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
        is False
    )


def test_changed_checkpoint_fails_closed() -> None:
    _, signature = signed_checkpoint()
    changed = replace(
        signature,
        checkpoint=create_checkpoint(
            origin="different-origin",
        ),
    )
    binding = create_binding()

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=changed,
            public_key_binding=binding,
        )
        is False
    )


def test_signature_from_other_key_fails_closed() -> None:
    _, signature = signed_checkpoint(
        scalar=1,
    )
    _, other = signed_checkpoint(
        scalar=2,
    )
    changed = replace(
        signature,
        signature=other.signature,
    )
    binding = create_binding(
        scalar=1,
    )

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=changed,
            public_key_binding=binding,
        )
        is False
    )


def test_changed_envelope_key_id_fails_closed() -> None:
    _, signature = signed_checkpoint()
    changed_identity = replace(
        signature.signing_key_identity,
        key_id="kms://security-admission/key-999",
    )
    changed = replace(
        signature,
        signing_key_identity=changed_identity,
    )
    binding = create_binding()

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=changed,
            public_key_binding=binding,
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
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=value,
            public_key_binding=create_binding(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "binding",
        b"binding",
        1,
        True,
        (),
    ),
)
def test_public_key_binding_rejects_invalid_type(
    value: object,
) -> None:
    _, signature = signed_checkpoint()

    with pytest.raises(
        TypeError,
        match="public_key_binding",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=value,
        )


def test_verification_preserves_inputs() -> None:
    _, signature = signed_checkpoint()
    binding = create_binding()
    checkpoint = signature.checkpoint
    identity = signature.signing_key_identity
    signature_bytes = signature.signature
    binding_identity = binding.signing_key_identity
    public_key_bytes = binding.public_key_bytes

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=signature,
            public_key_binding=binding,
        )
        is True
    )

    assert signature.checkpoint is checkpoint
    assert signature.signing_key_identity is identity
    assert signature.signature is signature_bytes
    assert binding.signing_key_identity is binding_identity
    assert binding.public_key_bytes is public_key_bytes


def test_verification_has_exact_boundary() -> None:
    parameters = inspect.signature(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding
    ).parameters

    assert tuple(parameters) == (
        "checkpoint_signature",
        "public_key_binding",
    )


def test_verification_receives_no_private_key() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding
    )

    assert "private_key" not in source
    assert "private_bytes" not in source


def test_verification_does_not_select_or_authorize_key() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding
    ).lower()
    forbidden = (
        "trusted",
        "registry",
        "resolver",
        "authority",
        "authorization",
        "admission_decision",
        "rejection",
    )

    assert all(
        token not in source
        for token in forbidden
    )
