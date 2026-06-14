from epics.ztc6_execution_provenance_binding.artifact_hash_binding import (
    ArtifactHashBinding,
)


def test_binding_is_deterministic():

    binding_1 = ArtifactHashBinding.compute(
        artifact_hash="artifact-001",
        execution_id="execution-001",
    )

    binding_2 = ArtifactHashBinding.compute(
        artifact_hash="artifact-001",
        execution_id="execution-001",
    )

    assert binding_1 == binding_2


def test_binding_changes_when_artifact_changes():

    binding_1 = ArtifactHashBinding.compute(
        artifact_hash="artifact-001",
        execution_id="execution-001",
    )

    binding_2 = ArtifactHashBinding.compute(
        artifact_hash="artifact-002",
        execution_id="execution-001",
    )

    assert binding_1 != binding_2
