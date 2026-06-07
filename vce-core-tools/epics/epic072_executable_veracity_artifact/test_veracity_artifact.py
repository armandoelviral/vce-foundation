from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def test_veracity_artifact_contains_six_layers():

    artifact = VeracityArtifact(
        identity={
            "identity_id": "id-001",
            "execution_id": "exec-001",
            "runtime_id": "runtime-001",
            "actor_type": "runner",
        },
        trust={
            "certificate_id": "cert-001",
            "trust_provider": "sigstore",
            "trust_timestamp": "2026-06-07T00:00:00Z",
        },
        provenance={
            "input_hash": "input-hash",
            "code_hash": "code-hash",
            "environment_hash": "environment-hash",
            "dependency_hash": "dependency-hash",
        },
        replay={
            "replay_uri": "wasm://vce_fuzz_runtime",
            "deterministic_checksum": "checksum-001",
            "runtime_version": "0.1.0",
            "sequence_number": 3,
        },
        evidence={
            "evidence_hash": "evidence-hash",
            "evidence_timestamp": "2026-06-07T00:00:00Z",
            "evidence_type": "DeterministicProof",
        },
        governance={
            "schema_version": "1.0",
            "policy_version": "1.0",
            "audit_scope": "runtime",
        },
    )

    as_dict = artifact.to_dict()

    assert "identity" in as_dict
    assert "trust" in as_dict
    assert "provenance" in as_dict
    assert "replay" in as_dict
    assert "evidence" in as_dict
    assert "governance" in as_dict


def test_veracity_artifact_is_immutable():

    artifact = VeracityArtifact(
        identity={},
        trust={},
        provenance={},
        replay={},
        evidence={},
        governance={},
    )

    try:
        artifact.identity = {}
        changed = True
    except Exception:
        changed = False

    assert changed is False
