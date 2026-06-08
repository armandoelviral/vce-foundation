from pathlib import Path


CONTRACT = Path(
    "epics/epic075_signed_veracity_proofs/signed_proof_contract.md"
)


def test_signed_proof_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_architecture():

    content = CONTRACT.read_text()

    assert "ENGINE RUNTIME" in content
    assert "EPIC075 ORCHESTRATION" in content
    assert "SIGNED VERACITY PROOF" in content


def test_contract_defines_signed_proof_fields():

    content = CONTRACT.read_text()

    assert "open_vce_payload" in content
    assert "artifact_hash" in content
    assert "ledger_sequence" in content
    assert "signature" in content
    assert "signing_key_id" in content
    assert "rekor_set" in content


def test_contract_defines_sigstore_future_integration():

    content = CONTRACT.read_text()

    assert "Fulcio identity certificate" in content
    assert "Rekor transparency log entry" in content
    assert "Signed Entry Timestamp" in content
