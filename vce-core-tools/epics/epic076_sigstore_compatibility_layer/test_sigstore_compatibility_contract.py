from pathlib import Path


CONTRACT = Path(
    "epics/epic076_sigstore_compatibility_layer/sigstore_compatibility_contract.md"
)


def test_sigstore_compatibility_contract_exists():

    assert CONTRACT.exists()


def test_contract_mentions_sigstore_components():

    content = CONTRACT.read_text()

    assert "OIDC" in content
    assert "Fulcio" in content
    assert "Rekor" in content
    assert "Transparency Log" in content


def test_contract_defines_oidc_identity_fields():

    content = CONTRACT.read_text()

    assert "oidc_issuer" in content
    assert "oidc_subject" in content
    assert "workflow_identity" in content
    assert "runner_identity" in content


def test_contract_defines_fulcio_fields():

    content = CONTRACT.read_text()

    assert "ephemeral certificate" in content
    assert "certificate_subject" in content
    assert "certificate_issuer" in content
    assert "public_key_binding" in content


def test_contract_defines_rekor_fields():

    content = CONTRACT.read_text()

    assert "transparency_log_entry" in content
    assert "log_index" in content
    assert "signed_entry_timestamp" in content
    assert "inclusion_proof" in content
