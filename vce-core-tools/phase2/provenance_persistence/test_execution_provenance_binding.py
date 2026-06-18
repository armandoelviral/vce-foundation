from phase2.provenance_persistence.execution_provenance_binding import (
    ExecutionProvenanceBinding,
)


def test_binding_contains_execution_id():

    binding = ExecutionProvenanceBinding(
        execution_id="exec-001",
        provenance_hash="hash-001",
    )

    assert binding.execution_id == "exec-001"


def test_binding_contains_provenance_hash():

    binding = ExecutionProvenanceBinding(
        execution_id="exec-001",
        provenance_hash="hash-001",
    )

    assert (
        binding.provenance_hash
        == "hash-001"
    )


def test_binding_serializes():

    binding = ExecutionProvenanceBinding(
        execution_id="exec-001",
        provenance_hash="hash-001",
    )

    assert binding.to_dict() == {
        "execution_id": "exec-001",
        "provenance_hash": "hash-001",
    }
