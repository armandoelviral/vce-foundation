from pathlib import Path


CONTRACT = Path(
    "epics/epic077_veracity_transparency_sidecar/privacy_preserving_data_flow.md"
)


def test_privacy_preserving_data_flow_contract_exists():

    assert CONTRACT.exists()


def test_contract_forbids_raw_sensitive_data_in_shared_volume():

    content = CONTRACT.read_text()

    assert "Raw sensitive data must never be written" in content
    assert "raw PHI" in content
    assert "raw PII" in content
    assert "raw biometrics" in content


def test_contract_allows_only_footprints_and_metadata():

    content = CONTRACT.read_text()

    assert "salted HMAC-SHA256 footprints" in content
    assert "logical metadata" in content
    assert "execution identifiers" in content


def test_sidecar_does_not_require_sensitive_data():

    content = CONTRACT.read_text()

    assert "must not require access to raw sensitive data" in content
    assert "without reading raw sensitive payloads" in content
