from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


def test_trust_record_creation():
    record = TrustRecord(
        trust_id="trust.001",
        actor_id="citizen.alpha",
        trust_amount=100,
        source_reference="evidence.001",
    )

    assert record.trust_id == "trust.001"
    assert record.actor_id == "citizen.alpha"
    assert record.trust_amount == 100
    assert record.source_reference == "evidence.001"


def test_rejects_empty_trust_id():
    try:
        TrustRecord(
            trust_id="",
            actor_id="citizen.alpha",
            trust_amount=100,
            source_reference="evidence.001",
        )
        assert False
    except ValueError as exc:
        assert "trust_id" in str(exc)


def test_rejects_non_positive_trust_amount():
    try:
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=0,
            source_reference="evidence.001",
        )
        assert False
    except ValueError as exc:
        assert "trust_amount" in str(exc)
