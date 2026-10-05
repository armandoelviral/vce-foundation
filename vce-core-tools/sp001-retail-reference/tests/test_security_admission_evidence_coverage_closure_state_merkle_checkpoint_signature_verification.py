import inspect
from dataclasses import replace

import pytest
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing import (
    sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)


KEY_ID = "kms://security-admission/key-001"


def p256_private_key(
    scalar: int = 1,
) -> ec.EllipticCurvePrivateKey:
    return ec.derive_private_key(
        scalar,
        ec.SECP256R1(),
    )


def signed_checkpoint(
    *,
    scalar: int = 1,
    key_id: str = KEY_ID,
    origin: str | None = None,
):
    checkpoint = (
        create_checkpoint()
        if origin is None
        else create_checkpoint(origin=origin)
    )
    private_key = p256_private_key(scalar)
    signature = (
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
            key_id=key_id,
            private_key=private_key,
        )
    )
    return private_key, signature


def verify(
    signature,
    *,
    scalar: int = 1,
    expected_key_id: str = KEY_ID,
) -> bool:
    return verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
        checkpoint_signature=signature,
        expected_key_id=expected_key_id,
        public_key=p256_private_key(scalar).public_key(),
    )


def test_exact_signature_verifies() -> None:
    _, signature = signed_checkpoint()

    assert verify(signature) is True


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
def test_multiple_p256_signing_keys_verify(
    scalar: int,
) -> None:
    _, signature = signed_checkpoint(
        scalar=scalar,
    )

    assert verify(
        signature,
        scalar=scalar,
    ) is True


def test_result_is_nominal_bool() -> None:
    _, signature = signed_checkpoint()

    assert type(verify(signature)) is bool


def test_wrong_expected_key_id_fails_closed() -> None:
    _, signature = signed_checkpoint()

    assert verify(
        signature,
        expected_key_id="kms://security-admission/key-002",
    ) is False


def test_wrong_public_key_fails_closed() -> None:
    _, signature = signed_checkpoint(
        scalar=1,
    )

    assert verify(
        signature,
        scalar=2,
    ) is False


def test_changed_checkpoint_fails_closed() -> None:
    _, signature = signed_checkpoint()
    changed = replace(
        signature,
        checkpoint=create_checkpoint(
            origin="different-origin",
        ),
    )

    assert verify(changed) is False


def test_signature_from_other_checkpoint_fails_closed() -> None:
    private_key, signature = signed_checkpoint()
    other = (
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=create_checkpoint(
                origin="different-origin",
            ),
            key_id=KEY_ID,
            private_key=private_key,
        )
    )
    changed = replace(
        signature,
        signature=other.signature,
    )

    assert verify(changed) is False


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

    assert verify(changed) is False


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

    assert verify(changed) is False


def test_changed_envelope_fingerprint_fails_closed() -> None:
    _, signature = signed_checkpoint()
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

    assert verify(changed) is False


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
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=value,
            expected_key_id=KEY_ID,
            public_key=p256_private_key().public_key(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"key-001",
        1,
        True,
        (),
        object(),
    ),
)
def test_expected_key_id_rejects_invalid_type(
    value: object,
) -> None:
    _, signature = signed_checkpoint()

    with pytest.raises(
        TypeError,
        match="expected_key_id",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=signature,
            expected_key_id=value,
            public_key=p256_private_key().public_key(),
        )


def test_expected_key_id_rejects_empty_value() -> None:
    _, signature = signed_checkpoint()

    with pytest.raises(
        ValueError,
        match="expected_key_id",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=signature,
            expected_key_id="",
            public_key=p256_private_key().public_key(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        b"public-key",
        "public-key",
        1,
        True,
        (),
    ),
)
def test_public_key_rejects_invalid_type(
    value: object,
) -> None:
    _, signature = signed_checkpoint()

    with pytest.raises(
        TypeError,
        match="public_key",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=signature,
            expected_key_id=KEY_ID,
            public_key=value,
        )


def test_public_key_rejects_wrong_curve() -> None:
    _, signature = signed_checkpoint()
    public_key = ec.derive_private_key(
        1,
        ec.SECP384R1(),
    ).public_key()

    with pytest.raises(
        ValueError,
        match="SECP256R1",
    ):
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=signature,
            expected_key_id=KEY_ID,
            public_key=public_key,
        )


def test_verification_preserves_inputs() -> None:
    private_key, signature = signed_checkpoint()
    public_key = private_key.public_key()
    identity = signature.signing_key_identity
    checkpoint = signature.checkpoint
    signature_bytes = signature.signature

    assert (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
            checkpoint_signature=signature,
            expected_key_id=KEY_ID,
            public_key=public_key,
        )
        is True
    )

    assert signature.checkpoint is checkpoint
    assert signature.signing_key_identity is identity
    assert signature.signature is signature_bytes


def test_verification_does_not_receive_private_key() -> None:
    parameters = inspect.signature(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature
    ).parameters

    assert tuple(parameters) == (
        "checkpoint_signature",
        "expected_key_id",
        "public_key",
    )


def test_verification_does_not_decide_or_authorize() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature
    )
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
