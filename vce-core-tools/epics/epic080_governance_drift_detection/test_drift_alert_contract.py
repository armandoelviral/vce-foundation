from pathlib import Path


CONTRACT = Path(
    "epics/epic080_governance_drift_detection/drift_alert_contract.md"
)


def test_drift_alert_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_required_alert_fields():

    content = CONTRACT.read_text()

    assert "alert_id" in content
    assert "model_id" in content
    assert "model_version" in content
    assert "drift_type" in content
    assert "expected_hash" in content
    assert "observed_hash" in content
    assert "blocking_required" in content


def test_contract_defines_drift_types():

    content = CONTRACT.read_text()

    assert "MODEL_HASH_MISMATCH" in content
    assert "WEIGHTS_HASH_MISMATCH" in content
    assert "RUNTIME_IMAGE_HASH_MISMATCH" in content
    assert "UNAPPROVED_MODEL_VERSION" in content
    assert "MISSING_GOVERNANCE_MANIFEST" in content


def test_contract_defines_required_response():

    content = CONTRACT.read_text()

    assert "emit a drift alert" in content
    assert "block transaction execution" in content
    assert "preserve evidence of the rejected attempt" in content
    assert "avoid anchoring the execution as valid" in content


def test_contract_preserves_scope_boundary():

    content = CONTRACT.read_text()

    assert "does not prove business" in content
    assert "medical" in content
    assert "financial" in content
    assert "ethical decision correctness" in content
