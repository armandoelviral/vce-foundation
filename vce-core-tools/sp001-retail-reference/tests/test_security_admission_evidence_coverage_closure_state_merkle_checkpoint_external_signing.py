import inspect

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_external_signing import (
    sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    create_binding,
)


KEY_ID = "kms://security-admission/key-001"


class ExternalSigner:
    def __init__(
        self,
        *,
        scalar: int = 1,
        key_id: str = KEY_ID,
    ) -> None:
        self._private_key = ec.derive_private_key(
            scalar,
            ec.SECP256R1(),
        )
        self._identity = create_binding(
            scalar=scalar,
            key_id=key_id,
        ).signing_key_identity
        self.received_payload: bytes | None = None
        self.calls = 0

    @property
    def signing_key_identity(self):
        return self._identity

    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        self.calls += 1
        self.received_payload = payload
        return self._private_key.sign(
            payload,
            ec.ECDSA(hashes.SHA256()),
        )


class WrongPayloadSigner(ExternalSigner):
    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        self.calls += 1
        self.received_payload = payload
        return self._private_key.sign(
            payload + b"-wrong",
            ec.ECDSA(hashes.SHA256()),
        )


class WrongKeySigner(ExternalSigner):
    def __init__(self) -> None:
        super().__init__(
            scalar=1,
            key_id=KEY_ID,
        )
        self._private_key = ec.derive_private_key(
            2,
            ec.SECP256R1(),
        )


class ReturnValueSigner(ExternalSigner):
    def __init__(
        self,
        value: object,
    ) -> None:
        super().__init__()
        self._value = value

    def sign(
        self,
        *,
        payload: bytes,
    ):
        self.calls += 1
        self.received_payload = payload
        return self._value


class InvalidIdentitySigner(ExternalSigner):
    @property
    def signing_key_identity(self):
        return "invalid-identity"


class FailingSigner(ExternalSigner):
    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        self.calls += 1
        self.received_payload = payload
        raise RuntimeError("external signer unavailable")


def sign(
    *,
    scalar: int = 1,
    key_id: str = KEY_ID,
):
    checkpoint = create_checkpoint()
    signer = ExternalSigner(
        scalar=scalar,
        key_id=key_id,
    )
    binding = create_binding(
        scalar=scalar,
        key_id=key_id,
    )

    result = (
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=checkpoint,
            signer=signer,
            public_key_binding=binding,
        )
    )

    return checkpoint, signer, binding, result


def test_external_signing_returns_nominal_envelope() -> None:
    checkpoint, _, binding, result = sign()

    assert isinstance(
        result,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
    )
    assert result.checkpoint is checkpoint
    assert (
        result.signing_key_identity
        == binding.signing_key_identity
    )
    assert result.signature_encoding == "ASN.1-DER"
    assert type(result.signature) is bytes
    assert result.signature


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
def test_multiple_external_keys_sign_and_verify(
    scalar: int,
) -> None:
    _, signer, binding, result = sign(
        scalar=scalar,
        key_id=(
            f"kms://security-admission/"
            f"key-{scalar}"
        ),
    )

    assert signer.calls == 1
    assert (
        result.signing_key_identity
        == binding.signing_key_identity
    )


def test_signer_receives_exact_canonical_payload() -> None:
    checkpoint, signer, _, _ = sign()
    expected = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    assert signer.received_payload == expected


def test_signer_is_called_exactly_once() -> None:
    _, signer, _, _ = sign()

    assert signer.calls == 1


def test_wrong_signer_identity_is_rejected_before_signing() -> None:
    checkpoint = create_checkpoint()
    signer = ExternalSigner(
        scalar=1,
        key_id="kms://security-admission/key-999",
    )
    binding = create_binding(
        scalar=1,
        key_id=KEY_ID,
    )

    with pytest.raises(
        ValueError,
        match="identity must match",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=checkpoint,
            signer=signer,
            public_key_binding=binding,
        )

    assert signer.calls == 0


def test_wrong_binding_key_is_rejected_before_signing() -> None:
    checkpoint = create_checkpoint()
    signer = ExternalSigner(
        scalar=1,
    )
    binding = create_binding(
        scalar=2,
        key_id=KEY_ID,
    )

    with pytest.raises(
        ValueError,
        match="identity must match",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=checkpoint,
            signer=signer,
            public_key_binding=binding,
        )

    assert signer.calls == 0


def test_wrong_payload_signature_fails_closed() -> None:
    signer = WrongPayloadSigner()
    binding = create_binding()

    with pytest.raises(
        ValueError,
        match="invalid checkpoint signature",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=binding,
        )

    assert signer.calls == 1


def test_wrong_private_key_signature_fails_closed() -> None:
    signer = WrongKeySigner()
    binding = create_binding()

    with pytest.raises(
        ValueError,
        match="invalid checkpoint signature",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=binding,
        )

    assert signer.calls == 1


@pytest.mark.parametrize(
    "value",
    (
        None,
        "signature",
        bytearray(b"signature"),
        memoryview(b"signature"),
        1,
        True,
        (),
        object(),
    ),
)
def test_non_bytes_signature_is_rejected(
    value: object,
) -> None:
    signer = ReturnValueSigner(value)

    with pytest.raises(
        TypeError,
        match="must return bytes",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=create_binding(),
        )


def test_empty_signature_is_rejected() -> None:
    signer = ReturnValueSigner(b"")

    with pytest.raises(
        ValueError,
        match="non-empty signature",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=create_binding(),
        )


def test_malformed_der_signature_is_rejected() -> None:
    signer = ReturnValueSigner(b"not-der")

    with pytest.raises(ValueError):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=create_binding(),
        )


def test_invalid_signer_identity_type_is_rejected() -> None:
    signer = InvalidIdentitySigner()

    with pytest.raises(
        TypeError,
        match="signer.signing_key_identity",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=create_binding(),
        )

    assert signer.calls == 0


def test_external_signer_failure_propagates_closed() -> None:
    signer = FailingSigner()

    with pytest.raises(
        RuntimeError,
        match="external signer unavailable",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=signer,
            public_key_binding=create_binding(),
        )

    assert signer.calls == 1


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "checkpoint",
        b"checkpoint",
        1,
        True,
        (),
    ),
)
def test_checkpoint_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="checkpoint",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=value,
            signer=ExternalSigner(),
            public_key_binding=create_binding(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "signer",
        b"signer",
        1,
        True,
        (),
    ),
)
def test_signer_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="signer",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=value,
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
    with pytest.raises(
        TypeError,
        match="public_key_binding",
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=create_checkpoint(),
            signer=ExternalSigner(),
            public_key_binding=value,
        )


def test_external_signing_preserves_inputs() -> None:
    checkpoint = create_checkpoint()
    signer = ExternalSigner()
    binding = create_binding()
    identity = binding.signing_key_identity
    public_key_bytes = binding.public_key_bytes

    result = (
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
            checkpoint=checkpoint,
            signer=signer,
            public_key_binding=binding,
        )
    )

    assert result.checkpoint is checkpoint
    assert binding.signing_key_identity is identity
    assert binding.public_key_bytes is public_key_bytes


def test_external_signing_has_exact_boundary() -> None:
    parameters = inspect.signature(
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer
    ).parameters

    assert tuple(parameters) == (
        "checkpoint",
        "signer",
        "public_key_binding",
    )


def test_service_receives_no_private_key() -> None:
    source = inspect.getsource(
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer
    )

    assert "private_key" not in source
    assert "private_bytes" not in source


def test_service_does_not_authorize_or_decide() -> None:
    source = inspect.getsource(
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer
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
