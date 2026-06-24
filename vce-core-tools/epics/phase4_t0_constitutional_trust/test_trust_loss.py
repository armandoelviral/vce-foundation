from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)


def test_trust_loss_creation():
    record = TrustLossRecord(
        loss_id="loss.001",
        actor_id="citizen.alpha",
        trust_loss_amount=40,
        reason="constitutional violation",
    )

    assert record.loss_id == "loss.001"
    assert record.actor_id == "citizen.alpha"
    assert record.trust_loss_amount == 40


def test_rejects_empty_loss_id():
    try:
        TrustLossRecord(
            loss_id="",
            actor_id="citizen.alpha",
            trust_loss_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "loss_id" in str(exc)


def test_rejects_non_positive_loss_amount():
    try:
        TrustLossRecord(
            loss_id="loss.001",
            actor_id="citizen.alpha",
            trust_loss_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "trust_loss_amount" in str(exc)
