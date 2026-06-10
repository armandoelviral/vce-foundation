from pathlib import Path


CONTRACT = Path(
    "epics/epic079_cryptographic_agility_framework/pqc_readiness_contract.md"
)


def test_pqc_readiness_contract_exists():

    assert CONTRACT.exists()


def test_contract_rejects_hardcoded_trust():

    content = CONTRACT.read_text()

    assert "must not hardcode trust" in content
    assert "single signature algorithm" in content
    assert "single hash algorithm" in content


def test_contract_requires_algorithm_identifiers():

    content = CONTRACT.read_text()

    assert "explicit signature_algorithm identifiers" in content
    assert "explicit hash_algorithm identifiers" in content
    assert "explicit cryptographic_epoch identifiers" in content


def test_contract_requires_multi_signature_transition():

    content = CONTRACT.read_text()

    assert "multi-signature transition proofs" in content
    assert "dual-signed proofs" in content
    assert "epoch-aware verification" in content


def test_contract_mentions_pqc_candidate_families():

    content = CONTRACT.read_text()

    assert "ML-DSA" in content
    assert "SLH-DSA" in content
    assert "future NIST-approved algorithms" in content


def test_contract_has_non_goals():

    content = CONTRACT.read_text()

    assert "production PQC implementation" in content
    assert "claiming quantum resistance" in content
