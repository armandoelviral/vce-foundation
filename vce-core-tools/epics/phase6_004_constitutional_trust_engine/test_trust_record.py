from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)


def test_trust_record_creation():
    record = TrustRecord(
        trust_id="trust.001",
        identity_id="identity.001",
        trust_delta=25,
    )

    assert record.trust_id == "trust.001"


def test_requires_trust_id():
    try:
        TrustRecord(
            "",
            "identity.001",
            25,
        )
        assert False
    except ValueError as exc:
        assert "trust_id" in str(exc)
