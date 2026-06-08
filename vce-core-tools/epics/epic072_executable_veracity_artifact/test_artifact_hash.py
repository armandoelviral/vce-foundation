from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def build_artifact():

    return VeracityArtifact(
        identity={"identity_id": "id-001"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "abc"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "xyz"},
        governance={"schema_version": "1.0"},
    )


def test_artifact_hash_is_deterministic():

    artifact_a = build_artifact()
    artifact_b = build_artifact()

    assert artifact_a.compute_hash() == artifact_b.compute_hash()


def test_artifact_hash_changes_when_content_changes():

    artifact_a = build_artifact()

    artifact_b = VeracityArtifact(
        identity={"identity_id": "id-002"},
        trust={"certificate_id": "cert-001"},
        provenance={"input_hash": "abc"},
        replay={"sequence_number": 3},
        evidence={"evidence_hash": "xyz"},
        governance={"schema_version": "1.0"},
    )

    assert artifact_a.compute_hash() != artifact_b.compute_hash()


def test_artifact_hash_is_sha256_length():

    artifact = build_artifact()

    digest = artifact.compute_hash()

    assert len(digest) == 64
