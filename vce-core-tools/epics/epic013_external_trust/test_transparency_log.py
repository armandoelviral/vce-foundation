from epics.epic013_external_trust.transparency_log import (
    TransparencyLog,
)


def test_creates_transparency_log_entry():

    log = TransparencyLog()

    artifact = {
        "name": "vce-runtime-attestation",
        "state_hash": "abc123",
    }

    entry = log.create_entry(
        artifact
    )

    assert entry is not None


def test_verifies_log_inclusion():

    log = TransparencyLog()

    artifact = {
        "name": "vce-runtime-attestation",
        "state_hash": "abc123",
    }

    entry = log.create_entry(
        artifact
    )

    assert log.verify_inclusion(
        entry
    ) is True
