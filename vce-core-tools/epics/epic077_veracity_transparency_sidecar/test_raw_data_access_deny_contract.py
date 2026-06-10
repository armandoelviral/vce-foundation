from pathlib import Path


CONTRACT = Path(
    "epics/epic077_veracity_transparency_sidecar/raw_data_access_deny_contract.md"
)


def test_raw_data_access_deny_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_security_property():

    content = CONTRACT.read_text()

    assert "prove execution without reading raw sensitive payloads" in content


def test_contract_denies_sensitive_data_classes():

    content = CONTRACT.read_text()

    assert "raw PHI" in content
    assert "raw PII" in content
    assert "raw biometrics" in content
    assert "raw financial transactions" in content
    assert "raw medical records" in content
    assert "raw inference inputs" in content


def test_contract_allows_only_evidence_classes():

    content = CONTRACT.read_text()

    assert "salted HMAC-SHA256 footprints" in content
    assert "artifact hashes" in content
    assert "anchor jobs" in content
    assert "signed proofs" in content
    assert "transparency receipts" in content


def test_contract_defines_kubernetes_mount_boundaries():

    content = CONTRACT.read_text()

    assert "must not mount" in content
    assert "application data volumes" in content
    assert "raw payload volumes" in content
    assert "proof queue volume" in content
    assert "receipt output volume" in content


def test_contract_defines_iam_boundaries():

    content = CONTRACT.read_text()

    assert "reading raw data buckets" in content
    assert "reading customer data secrets" in content
    assert "deleting evidence ledger objects" in content
    assert "bypassing WORM retention" in content
    assert "kms:GetPublicKey" in content
