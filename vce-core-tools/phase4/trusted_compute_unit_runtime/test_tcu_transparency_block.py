from phase4.trusted_compute_unit_runtime.tcu_transparency_block import (
    TcuTransparencyBlock,
)


def test_contains_ledger_index():

    block = TcuTransparencyBlock(
        ledger_index=4201,
        parent_block_hash="parent-001",
        merkle_root="root-001",
        merkle_inclusion_proof=["proof-1", "proof-2"],
    )

    assert block.ledger_index == 4201


def test_contains_parent_hash():

    block = TcuTransparencyBlock(
        ledger_index=4201,
        parent_block_hash="parent-001",
        merkle_root="root-001",
        merkle_inclusion_proof=["proof-1", "proof-2"],
    )

    assert block.parent_block_hash == "parent-001"


def test_contains_merkle_root():

    block = TcuTransparencyBlock(
        ledger_index=4201,
        parent_block_hash="parent-001",
        merkle_root="root-001",
        merkle_inclusion_proof=["proof-1", "proof-2"],
    )

    assert block.merkle_root == "root-001"


def test_contains_proof():

    block = TcuTransparencyBlock(
        ledger_index=4201,
        parent_block_hash="parent-001",
        merkle_root="root-001",
        merkle_inclusion_proof=["proof-1", "proof-2"],
    )

    assert len(block.merkle_inclusion_proof) == 2


def test_serializes():

    block = TcuTransparencyBlock(
        ledger_index=4201,
        parent_block_hash="parent-001",
        merkle_root="root-001",
        merkle_inclusion_proof=["proof-1", "proof-2"],
    )

    assert block.to_dict() == {
        "ledger_index": 4201,
        "parent_block_hash": "parent-001",
        "merkle_root": "root-001",
        "merkle_inclusion_proof": [
            "proof-1",
            "proof-2",
        ],
    }
