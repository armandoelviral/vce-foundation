from epics.epic079_cryptographic_agility_framework.cryptographic_epoch import (
    CryptographicEpoch,
)


def test_epoch_creation():

    epoch = CryptographicEpoch(
        epoch_id="epoch-001",
        signature_algorithm="ECDSA_P256",
        hash_algorithm="SHA256",
        active=True,
        introduced_at="2026-01-01",
    )

    assert epoch.epoch_id == "epoch-001"


def test_epoch_contains_signature_algorithm():

    epoch = CryptographicEpoch(
        epoch_id="epoch-001",
        signature_algorithm="ECDSA_P256",
        hash_algorithm="SHA256",
        active=True,
        introduced_at="2026-01-01",
    )

    assert epoch.signature_algorithm == "ECDSA_P256"


def test_epoch_contains_hash_algorithm():

    epoch = CryptographicEpoch(
        epoch_id="epoch-001",
        signature_algorithm="ECDSA_P256",
        hash_algorithm="SHA256",
        active=True,
        introduced_at="2026-01-01",
    )

    assert epoch.hash_algorithm == "SHA256"


def test_epoch_serialization():

    epoch = CryptographicEpoch(
        epoch_id="epoch-001",
        signature_algorithm="ECDSA_P256",
        hash_algorithm="SHA256",
        active=True,
        introduced_at="2026-01-01",
    )

    payload = epoch.to_dict()

    assert payload["epoch_id"] == "epoch-001"
    assert payload["signature_algorithm"] == "ECDSA_P256"
    assert payload["hash_algorithm"] == "SHA256"
