from epics.phase4_037_constitutional_prosperity.prosperity_audit import (
    audit_prosperity,
)
from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


def test_prosperity_audit():
    records = [
        ProsperityRecord(
            "prosperity.001",
            "sustainability.001",
            100,
            "growth",
        )
    ]

    losses = [
        ProsperityLossRecord(
            "loss.001",
            "prosperity.001",
            40,
            "economic contraction",
        )
    ]

    audit = audit_prosperity(records, losses)

    assert audit["prosperity_count"] == 1
    assert audit["loss_count"] == 1
    assert audit["total_prosperity"] == 100
    assert audit["total_loss"] == 40


def test_empty_prosperity_audit():
    audit = audit_prosperity([], [])

    assert audit["prosperity_count"] == 0
    assert audit["loss_count"] == 0
