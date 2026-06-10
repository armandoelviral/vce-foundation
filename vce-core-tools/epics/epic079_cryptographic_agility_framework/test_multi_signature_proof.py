from epics.epic079_cryptographic_agility_framework.multi_signature_proof import (
    MultiSignatureProof,
    ProofSignature,
)


def build_multi_signature_proof():

    return MultiSignatureProof(
        artifact_hash="artifact-hash-001",
        signatures=[
            ProofSignature(
                signature_id="sig-001",
                algorithm_id="ecdsa-p256",
                signature_value="legacy-signature",
                cryptographic_epoch="epoch-001",
            ),
            ProofSignature(
                signature_id="sig-002",
                algorithm_id="ml-dsa-65",
                signature_value="pqc-signature",
                cryptographic_epoch="epoch-002",
            ),
        ],
    )


def test_multi_signature_proof_creation():

    proof = build_multi_signature_proof()

    assert proof.artifact_hash == "artifact-hash-001"


def test_multi_signature_proof_counts_signatures():

    proof = build_multi_signature_proof()

    assert proof.signature_count() == 2


def test_multi_signature_proof_lists_algorithms():

    proof = build_multi_signature_proof()

    assert proof.algorithms() == [
        "ecdsa-p256",
        "ml-dsa-65",
    ]


def test_multi_signature_proof_detects_legacy_algorithm():

    proof = build_multi_signature_proof()

    assert proof.has_algorithm(
        "ecdsa-p256"
    ) is True


def test_multi_signature_proof_detects_pqc_algorithm():

    proof = build_multi_signature_proof()

    assert proof.has_algorithm(
        "ml-dsa-65"
    ) is True
