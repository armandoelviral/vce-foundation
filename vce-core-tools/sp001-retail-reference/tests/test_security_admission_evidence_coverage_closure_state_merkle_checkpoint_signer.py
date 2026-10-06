import inspect
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signer import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    create_binding,
)


class StubSigner:
    def __init__(
        self,
        identity: (
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
        ),
    ) -> None:
        self._identity = identity
        self.received_payload: bytes | None = None

    @property
    def signing_key_identity(
        self,
    ) -> (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    ):
        return self._identity

    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        self.received_payload = payload
        return b"stub-signature"


class MissingIdentity:
    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        return payload


class MissingSign:
    @property
    def signing_key_identity(
        self,
    ):
        return create_binding().signing_key_identity


def create_signer() -> StubSigner:
    return StubSigner(
        create_binding().signing_key_identity
    )


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(
        create_signer(),
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
    )


def test_protocol_accepts_structural_implementation() -> None:
    signer = create_signer()

    assert (
        signer.__class__
        is not SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner
    )
    assert isinstance(
        signer,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
    )


def test_missing_identity_does_not_conform() -> None:
    assert not isinstance(
        MissingIdentity(),
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
    )


def test_missing_sign_does_not_conform() -> None:
    assert not isinstance(
        MissingSign(),
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
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
def test_unrelated_values_do_not_conform(
    value: object,
) -> None:
    assert not isinstance(
        value,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
    )


def test_protocol_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner()


def test_identity_property_returns_nominal_identity() -> None:
    signer = create_signer()

    assert isinstance(
        signer.signing_key_identity,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
    )


def test_sign_receives_exact_payload() -> None:
    signer = create_signer()
    payload = b"canonical-checkpoint-payload"

    signature = signer.sign(
        payload=payload,
    )

    assert signer.received_payload is payload
    assert signature == b"stub-signature"


def test_sign_has_keyword_only_payload() -> None:
    parameters = inspect.signature(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner.sign
    ).parameters

    assert tuple(parameters) == (
        "self",
        "payload",
    )
    assert (
        parameters["payload"].kind
        is inspect.Parameter.KEYWORD_ONLY
    )


def test_sign_annotations_are_portable_bytes() -> None:
    hints = get_type_hints(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner.sign
    )

    assert hints["payload"] is bytes
    assert hints["return"] is bytes


def test_identity_annotation_is_nominal() -> None:
    hints = get_type_hints(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner.signing_key_identity.fget
    )

    assert (
        hints["return"]
        is SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    )


def test_protocol_exposes_exact_public_members() -> None:
    public_members = tuple(
        name
        for name, value in vars(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner
        ).items()
        if (
            not name.startswith("_")
            and (
                inspect.isfunction(value)
                or isinstance(value, property)
            )
        )
    )

    assert public_members == (
        "signing_key_identity",
        "sign",
    )


def test_protocol_exposes_no_private_key() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner
    )

    assert "private_key" not in source
    assert "private_bytes" not in source


def test_protocol_does_not_execute_or_decide() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner
    ).lower()
    forbidden = (
        "kms",
        "hsm",
        ".verify",
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
