from pathlib import Path


FLOW = Path(
    "epics/epic071_operational_veracity_pipeline/drift_auditing_flow.md"
)


def test_drift_auditing_flow_exists():

    assert FLOW.exists()


def test_flow_defines_audit_inputs():

    content = FLOW.read_text()

    assert "ledger_sequence" in content
    assert "artifact_id" in content
    assert "original_artifact_hash" in content
    assert "original_state_hash" in content
    assert "original_replay_uri" in content
    assert "original_deterministic_checksum" in content


def test_flow_defines_audit_process():

    content = FLOW.read_text()

    assert "read historical ledger entry" in content
    assert "recover original VeracityArtifact" in content
    assert "verify replay artifact checksum" in content
    assert "restore hermetic execution boundary" in content
    assert "recompute state hash" in content


def test_flow_defines_audit_result():

    content = FLOW.read_text()

    assert "audit_id" in content
    assert "recomputed_state_hash" in content
    assert "drift_detected" in content
    assert "audit_timestamp" in content
    assert "audit_status" in content


def test_flow_defines_drift_conditions():

    content = FLOW.read_text()

    assert "recomputed_state_hash differs from original_state_hash" in content
    assert "replay artifact checksum does not match" in content
    assert "hermetic execution boundary cannot be restored" in content
    assert "required historical evidence is missing" in content
