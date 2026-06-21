from phase4.real_zkvm_integration.risc_zero_prover_adapter import (
    RiscZeroProverAdapter,
)


def test_adapter_exposes_prover_type():

    adapter = RiscZeroProverAdapter()

    assert (
        adapter.prover_type()
        == "RISC_ZERO"
    )


def test_generates_proof_request():

    adapter = RiscZeroProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["execution_request_id"]
        == "request-001"
    )


def test_generates_risc_zero_proof():

    adapter = RiscZeroProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["prover_type"]
        == "RISC_ZERO"
    )


def test_proof_contains_status():

    adapter = RiscZeroProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["status"]
        == "PROOF_GENERATED"
    )


def test_proof_contains_placeholder_hash():

    adapter = RiscZeroProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["proof_hash"]
        == "risc-zero-proof-request-001"
    )
