import inspect
from dataclasses import FrozenInstanceError, fields

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    derive_identity,
    p256_public_key,
)


def canonical_signature(
    r_value: int = 1,
    s_value: int = 2,
) -> bytes:
    return encode_dss_signature(
        r_value,
        s_value,
    )


def create_signature(
    *,
    signature: bytes | None = None,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature:
    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=create_checkpoint(),
            signing_key_identity=derive_identity(),
            signature_encoding="ASN.1-DER",
            signature=(
                canonical_signature()
                if signature is None
                else signature
            ),
        )
    )


def test_signature_fields_are_exact() -> None:
    signature_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    )

    assert tuple(field.name for field in signature_fields) == (
        "checkpoint",
        "signing_key_identity",
        "signature_encoding",
        "signature",
    )
    assert tuple(field.type for field in signature_fields) == (
        type(create_checkpoint()),
        type(derive_identity()),
        str,
        bytes,
    )


def test_signature_is_immutable_and_slotted() -> None:
    signed_checkpoint = create_signature()

    assert not hasattr(signed_checkpoint, "__dict__")

    with pytest.raises(FrozenInstanceError):
        signed_checkpoint.signature = b"x"  # type: ignore[misc]


def test_signature_encoding_constant_is_exact() -> None:
    assert (
        SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING
        == "ASN.1-DER"
    )


def test_exact_references_and_bytes_are_preserved() -> None:
    checkpoint = create_checkpoint()
    identity = derive_identity()
    signature = canonical_signature(3, 5)

    signed_checkpoint = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=checkpoint,
            signing_key_identity=identity,
            signature_encoding="ASN.1-DER",
            signature=signature,
        )
    )

    assert signed_checkpoint.checkpoint is checkpoint
    assert signed_checkpoint.signing_key_identity is identity
    assert signed_checkpoint.signature is signature
    assert signed_checkpoint.signature_encoding == "ASN.1-DER"


@pytest.mark.parametrize(
    ("r_value", "s_value"),
    (
        (1, 1),
        (1, 2),
        (2, 1),
        (3, 5),
        (65537, 104729),
        ((1 << 255) - 19, (1 << 254) + 7),
    ),
)
def test_canonical_der_signatures_are_preserved(
    r_value: int,
    s_value: int,
) -> None:
    signature = canonical_signature(
        r_value,
        s_value,
    )
    signed_checkpoint = create_signature(
        signature=signature,
    )

    assert signed_checkpoint.signature == signature
    assert decode_dss_signature(
        signed_checkpoint.signature
    ) == (
        r_value,
        s_value,
    )


def test_real_p256_signature_is_accepted() -> None:
    private_key = ec.derive_private_key(
        7,
        ec.SECP256R1(),
    )
    signature = private_key.sign(
        b"canonical-checkpoint-payload",
        ec.ECDSA(hashes.SHA256()),
    )

    signed_checkpoint = create_signature(
        signature=signature,
    )

    assert signed_checkpoint.signature == signature


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "checkpoint",
        {},
        object(),
    ),
)
def test_checkpoint_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=invalid_value,  # type: ignore[arg-type]
            signing_key_identity=derive_identity(),
            signature_encoding="ASN.1-DER",
            signature=canonical_signature(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "identity",
        {},
        object(),
    ),
)
def test_signing_key_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "signing_key_identity must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=create_checkpoint(),
            signing_key_identity=invalid_value,  # type: ignore[arg-type]
            signature_encoding="ASN.1-DER",
            signature=canonical_signature(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"ASN.1-DER",
        object(),
    ),
)
def test_signature_encoding_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "signature_encoding must be a str"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=create_checkpoint(),
            signing_key_identity=derive_identity(),
            signature_encoding=invalid_value,  # type: ignore[arg-type]
            signature=canonical_signature(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "DER",
        "ASN1-DER",
        "IEEE-P1363",
        "RAW",
        "asn.1-der",
    ),
)
def test_signature_encoding_rejects_other_profiles(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "signature_encoding must be ASN.1-DER"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=create_checkpoint(),
            signing_key_identity=derive_identity(),
            signature_encoding=invalid_value,
            signature=canonical_signature(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "signature",
        bytearray(b"signature"),
        memoryview(b"signature"),
        object(),
    ),
)
def test_signature_requires_exact_bytes(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="signature must be bytes",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=create_checkpoint(),
            signing_key_identity=derive_identity(),
            signature_encoding="ASN.1-DER",
            signature=invalid_value,  # type: ignore[arg-type]
        )


def test_signature_rejects_empty_bytes() -> None:
    with pytest.raises(
        ValueError,
        match="signature must not be empty",
    ):
        create_signature(signature=b"")


@pytest.mark.parametrize(
    "invalid_value",
    (
        b"x",
        b"signature",
        b"\x30\x00",
        b"\x30\x03\x02\x01\x01",
        b"\x00" * 64,
        b"\xff" * 72,
    ),
)
def test_signature_rejects_malformed_der(
    invalid_value: bytes,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "signature must be a valid ASN.1-DER "
            "ECDSA signature"
        ),
    ):
        create_signature(signature=invalid_value)


@pytest.mark.parametrize(
    "invalid_value",
    (
        encode_dss_signature(0, 1),
        encode_dss_signature(1, 0),
        encode_dss_signature(0, 0),
    ),
)
def test_signature_requires_positive_components(
    invalid_value: bytes,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "signature must be a canonical ASN.1-DER "
            "ECDSA signature"
        ),
    ):
        create_signature(signature=invalid_value)


def test_signature_contract_contains_no_private_key() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
        )
    }

    assert "private_key" not in field_names
    assert "private_key_bytes" not in field_names
    assert "credential" not in field_names
    assert "secret" not in field_names


def test_signature_contract_does_not_claim_verification() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    )

    assert ".verify(" not in source
    assert "InvalidSignature" not in source


def test_signature_contract_grants_no_authority() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
        )
    }

    assert "authority" not in field_names
    assert "authorization" not in field_names
    assert "decision" not in field_names
    assert "admission_status" not in field_names


def test_unused_public_key_is_not_embedded() -> None:
    public_key = p256_public_key()
    signed_checkpoint = create_signature()

    assert not hasattr(signed_checkpoint, "public_key")
    assert public_key is not signed_checkpoint.signing_key_identity
