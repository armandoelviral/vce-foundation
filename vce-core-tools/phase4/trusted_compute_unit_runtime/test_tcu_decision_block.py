from phase4.trusted_compute_unit_runtime.tcu_decision_block import (
    TcuDecisionBlock,
)


def test_contains_verdict():

    block = TcuDecisionBlock(
        verdict="APPROVED",
        execution_status="SUCCESS",
        compute_gas_used=42100,
        system_state_root="state-root-001",
    )

    assert block.verdict == "APPROVED"


def test_contains_execution_status():

    block = TcuDecisionBlock(
        verdict="APPROVED",
        execution_status="SUCCESS",
        compute_gas_used=42100,
        system_state_root="state-root-001",
    )

    assert block.execution_status == "SUCCESS"


def test_contains_compute_gas_used():

    block = TcuDecisionBlock(
        verdict="APPROVED",
        execution_status="SUCCESS",
        compute_gas_used=42100,
        system_state_root="state-root-001",
    )

    assert block.compute_gas_used == 42100


def test_contains_system_state_root():

    block = TcuDecisionBlock(
        verdict="APPROVED",
        execution_status="SUCCESS",
        compute_gas_used=42100,
        system_state_root="state-root-001",
    )

    assert block.system_state_root == "state-root-001"


def test_serializes():

    block = TcuDecisionBlock(
        verdict="APPROVED",
        execution_status="SUCCESS",
        compute_gas_used=42100,
        system_state_root="state-root-001",
    )

    assert block.to_dict() == {
        "verdict": "APPROVED",
        "execution_status": "SUCCESS",
        "compute_gas_used": 42100,
        "system_state_root": "state-root-001",
    }
