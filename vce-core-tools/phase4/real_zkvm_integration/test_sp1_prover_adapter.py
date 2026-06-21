from phase4.real_zkvm_integration.sp1_prover_adapter import (
    SP1ProverAdapter,
)


def test_adapter_exposes_prover_type():

    adapter = SP1ProverAdapter()

    assert (
        adapter.prover_type()
        == "SP1"
    )


def test_generates_proof_request():

    adapter = SP1ProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["execution_request_id"]
        == "request-001"
    )


def test_generates_sp1_proof():

    adapter = SP1ProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["prover_type"]
        == "SP1"
    )


def test_proof_contains_status():

    adapter = SP1ProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["status"]
        == "PROOF_GENERATED"
    )


def test_proof_contains_placeholder_hash():

    adapter = SP1ProverAdapter()

    proof = adapter.generate_proof(
        execution_request_id="request-001"
    )

    assert (
        proof["proof_hash"]
        == "sp1-proof-request-001"
    )
