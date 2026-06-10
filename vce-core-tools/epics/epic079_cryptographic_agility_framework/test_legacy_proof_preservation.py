from epics.epic079_cryptographic_agility_framework.multi_signature_proof import (
    MultiSignatureProof,
    ProofSignature,
)

from epics.epic079_cryptographic_agility_framework.legacy_proof_preservation import (
    LegacyProofPreservation,
)


def build_epoch_1_proof():

    return MultiSignatureProof(
        artifact_hash="artifact-001",
        signatures=[
            ProofSignature(
                signature_id="sig-001",
                algorithm_id="ecdsa-p256",
                signature_value="legacy",
                cryptographic_epoch="epoch-001",
            )
        ],
    )


def build_epoch_2_proof():

    return MultiSignatureProof(
        artifact_hash="artifact-002",
        signatures=[
            ProofSignature(
                signature_id="sig-002",
                algorithm_id="ml-dsa-65",
                signature_value="future",
                cryptographic_epoch="epoch-002",
            )
        ],
    )


def test_preservation_accepts_epoch_1_proof():

    verifier = (
        LegacyProofPreservation(
            supported_epochs=[
                "epoch-001",
                "epoch-002",
            ]
        )
    )

    assert verifier.can_verify(
        build_epoch_1_proof()
    ) is True


def test_preservation_accepts_epoch_2_proof():

    verifier = (
        LegacyProofPreservation(
            supported_epochs=[
                "epoch-001",
                "epoch-002",
            ]
        )
    )

    assert verifier.can_verify(
        build_epoch_2_proof()
    ) is True


def test_preservation_rejects_unknown_epoch():

    proof = MultiSignatureProof(
        artifact_hash="artifact-003",
        signatures=[
            ProofSignature(
                signature_id="sig-003",
                algorithm_id="future",
                signature_value="x",
                cryptographic_epoch="epoch-999",
            )
        ],
    )

    verifier = (
        LegacyProofPreservation(
            supported_epochs=[
                "epoch-001",
                "epoch-002",
            ]
        )
    )

    assert verifier.can_verify(
        proof
    ) is False


def test_preservation_supports_migration_windows():

    proof = MultiSignatureProof(
        artifact_hash="artifact-004",
        signatures=[
            ProofSignature(
                signature_id="sig-001",
                algorithm_id="ecdsa-p256",
                signature_value="legacy",
                cryptographic_epoch="epoch-001",
            ),
            ProofSignature(
                signature_id="sig-002",
                algorithm_id="ml-dsa-65",
                signature_value="future",
                cryptographic_epoch="epoch-002",
            ),
        ],
    )

    verifier = (
        LegacyProofPreservation(
            supported_epochs=[
                "epoch-001",
                "epoch-002",
            ]
        )
    )

    assert verifier.can_verify(
        proof
    ) is True
