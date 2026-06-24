from epics.phase4_t0_constitutional_trust.trust_accrual import (
    calculate_total_trust,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


def test_calculates_total_trust():
    records = [
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=100,
            source_reference="evidence.001",
        ),
        TrustRecord(
            trust_id="trust.002",
            actor_id="citizen.alpha",
            trust_amount=50,
            source_reference="evidence.002",
        ),
    ]

    assert calculate_total_trust(records) == 150


def test_empty_trust():
    assert calculate_total_trust([]) == 0


def test_single_trust():
    records = [
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=75,
            source_reference="evidence.001",
        )
    ]

    assert calculate_total_trust(records) == 75
