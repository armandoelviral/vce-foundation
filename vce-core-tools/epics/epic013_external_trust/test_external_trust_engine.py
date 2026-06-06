from epics.epic013_external_trust.external_trust_engine import (
    ExternalTrustEngine,
)


def test_external_trust_engine_verifies_certificate_and_artifact():

    engine = ExternalTrustEngine()

    certificate = {
        "issuer": "github-actions",
        "subject": "repo:vce-foundation",
        "repository": "vce-core-tools",
        "expires_at": "2026-12-31",
    }

    artifact = {
        "name": "runtime-attestation",
        "hash": "abc123",
    }

    assert engine.verify(
        certificate,
        artifact,
    ) is True
