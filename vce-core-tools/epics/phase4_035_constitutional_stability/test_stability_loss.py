from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)


def test_stability_loss_creation():
    record = StabilityLossRecord(
        loss_id="loss.001",
        stability_id="stability.001",
        loss_amount=40,
        reason="liquidity shock",
    )

    assert record.loss_amount == 40


def test_rejects_empty_loss_id():
    try:
        StabilityLossRecord("", "stability.001", 40, "invalid")
        assert False
    except ValueError as exc:
        assert "loss_id" in str(exc)


def test_rejects_non_positive_loss_amount():
    try:
        StabilityLossRecord("loss.001", "stability.001", 0, "invalid")
        assert False
    except ValueError as exc:
        assert "loss_amount" in str(exc)
