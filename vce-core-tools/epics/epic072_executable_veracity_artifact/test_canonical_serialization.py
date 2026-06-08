from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def build_artifact():

    return VeracityArtifact(
        identity={"b": 2, "a": 1},
        trust={"z": 2, "y": 1},
        provenance={},
        replay={},
        evidence={},
        governance={},
    )


def test_canonical_json_is_deterministic():

    artifact_a = build_artifact()
    artifact_b = build_artifact()

    assert (
        artifact_a.to_canonical_json()
        ==
        artifact_b.to_canonical_json()
    )


def test_canonical_json_sorts_keys():

    artifact = build_artifact()

    payload = artifact.to_canonical_json()

    assert '"a":1' in payload
    assert '"b":2' in payload

    assert payload.index('"a":1') < payload.index('"b":2')
