from phase2.provenance_persistence.artifact_provenance_binding import (
    ArtifactProvenanceBinding,
)


def test_binding_contains_artifact_id():

    binding = ArtifactProvenanceBinding(
        artifact_id="artifact-001",
        provenance_hash="hash-001",
    )

    assert binding.artifact_id == "artifact-001"


def test_binding_contains_provenance_hash():

    binding = ArtifactProvenanceBinding(
        artifact_id="artifact-001",
        provenance_hash="hash-001",
    )

    assert (
        binding.provenance_hash
        == "hash-001"
    )


def test_binding_serializes():

    binding = ArtifactProvenanceBinding(
        artifact_id="artifact-001",
        provenance_hash="hash-001",
    )

    assert binding.to_dict() == {
        "artifact_id": "artifact-001",
        "provenance_hash": "hash-001",
    }
