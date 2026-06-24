from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)


def test_prosperity_loss_creation():
    record = ProsperityLossRecord(
        loss_id="loss.001",
        prosperity_id="prosperity.001",
        loss_amount=40,
        reason="economic contraction",
    )

    assert record.loss_id == "loss.001"
    assert record.prosperity_id == "prosperity.001"
    assert record.loss_amount == 40


def test_rejects_empty_loss_id():
    try:
        ProsperityLossRecord(
            loss_id="",
            prosperity_id="prosperity.001",
            loss_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "loss_id" in str(exc)


def test_rejects_non_positive_loss_amount():
    try:
        ProsperityLossRecord(
            loss_id="loss.001",
            prosperity_id="prosperity.001",
            loss_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "loss_amount" in str(exc)
