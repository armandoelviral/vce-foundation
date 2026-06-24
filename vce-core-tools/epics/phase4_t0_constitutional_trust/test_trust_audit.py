from epics.phase4_t0_constitutional_trust.trust_audit import (
    audit_trust,
)
from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


def test_trust_audit():
    trust = [
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=100,
            source_reference="evidence.001",
        )
    ]

    losses = [
        TrustLossRecord(
            loss_id="loss.001",
            actor_id="citizen.alpha",
            trust_loss_amount=40,
            reason="violation",
        )
    ]

    audit = audit_trust(
        trust_records=trust,
        trust_losses=losses,
    )

    assert audit["total_trust"] == 100
    assert audit["total_loss"] == 40


def test_empty_audit():
    audit = audit_trust([], [])

    assert audit["total_trust"] == 0
    assert audit["total_loss"] == 0
