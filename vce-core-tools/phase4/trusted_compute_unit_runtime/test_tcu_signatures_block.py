from phase4.trusted_compute_unit_runtime.tcu_signatures_block import (
    TcuSignaturesBlock,
)


def test_contains_ed25519():

    block = TcuSignaturesBlock(
        classical_ed25519="ed25519-sig-001",
        post_quantum_mldsa65="mldsa65-sig-001",
    )

    assert block.classical_ed25519 == "ed25519-sig-001"


def test_contains_mldsa():

    block = TcuSignaturesBlock(
        classical_ed25519="ed25519-sig-001",
        post_quantum_mldsa65="mldsa65-sig-001",
    )

    assert block.post_quantum_mldsa65 == "mldsa65-sig-001"


def test_serializes():

    block = TcuSignaturesBlock(
        classical_ed25519="ed25519-sig-001",
        post_quantum_mldsa65="mldsa65-sig-001",
    )

    assert block.to_dict() == {
        "classical_ed25519": "ed25519-sig-001",
        "post_quantum_mldsa65": "mldsa65-sig-001",
    }
