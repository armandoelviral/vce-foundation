from epics.phase4_035_constitutional_stability.stability_audit import (
    audit_stability,
)
from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


def test_stability_audit():
    records = [StabilityRecord("s1", "treasury.001", 100, "continuity")]
    losses = [StabilityLossRecord("l1", "s1", 40, "liquidity shock")]

    audit = audit_stability(records, losses)

    assert audit["stability_count"] == 1
    assert audit["loss_count"] == 1
    assert audit["total_stability"] == 100
    assert audit["total_loss"] == 40


def test_empty_stability_audit():
    audit = audit_stability([], [])

    assert audit["stability_count"] == 0
    assert audit["loss_count"] == 0
    assert audit["total_stability"] == 0
    assert audit["total_loss"] == 0
