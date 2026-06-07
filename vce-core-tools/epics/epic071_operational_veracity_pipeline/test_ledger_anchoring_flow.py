from pathlib import Path


FLOW = Path(
    "epics/epic071_operational_veracity_pipeline/ledger_anchoring_flow.md"
)


def test_ledger_anchoring_flow_exists():

    assert FLOW.exists()


def test_flow_defines_anchoring_preconditions():

    content = FLOW.read_text()

    assert "schema validation" in content
    assert "required field validation" in content
    assert "content hash validation" in content
    assert "replay metadata validation" in content
    assert "trust metadata validation" in content


def test_flow_defines_canonical_serialization():

    content = FLOW.read_text()

    assert "stable key ordering" in content
    assert "deterministic JSON encoding" in content
    assert "reproducible byte representation" in content


def test_flow_defines_commit_receipt():

    content = FLOW.read_text()

    assert "artifact_id" in content
    assert "artifact_hash" in content
    assert "ledger_sequence" in content
    assert "ledger_state_hash" in content
    assert "commit_timestamp" in content
    assert "anchoring_status" in content


def test_flow_defines_failure_conditions():

    content = FLOW.read_text()

    assert "artifact schema is invalid" in content
    assert "required fields are missing" in content
    assert "content hash mismatch is detected" in content
    assert "ledger append fails" in content
