from phase4.trusted_compute_unit_runtime.tcu_proof_block import (
    TcuProofBlock,
)


def test_contains_backend():

    block = TcuProofBlock(
        proof_backend="SP1",
        proof_status="VERIFIED",
        verification_key="vk-001",
        proof_hash="proof-hash-001",
    )

    assert block.proof_backend == "SP1"


def test_contains_status():

    block = TcuProofBlock(
        proof_backend="SP1",
        proof_status="VERIFIED",
        verification_key="vk-001",
        proof_hash="proof-hash-001",
    )

    assert block.proof_status == "VERIFIED"


def test_contains_vk():

    block = TcuProofBlock(
        proof_backend="SP1",
        proof_status="VERIFIED",
        verification_key="vk-001",
        proof_hash="proof-hash-001",
    )

    assert block.verification_key == "vk-001"


def test_contains_proof_hash():

    block = TcuProofBlock(
        proof_backend="SP1",
        proof_status="VERIFIED",
        verification_key="vk-001",
        proof_hash="proof-hash-001",
    )

    assert block.proof_hash == "proof-hash-001"


def test_serializes():

    block = TcuProofBlock(
        proof_backend="SP1",
        proof_status="VERIFIED",
        verification_key="vk-001",
        proof_hash="proof-hash-001",
    )

    assert block.to_dict() == {
        "proof_backend": "SP1",
        "proof_status": "VERIFIED",
        "verification_key": "vk-001",
        "proof_hash": "proof-hash-001",
    }
