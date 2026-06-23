from epics.phase4_030_constitutional_risk.risk_record import RiskRecord


def test_risk_record_creation():
    record = RiskRecord(
        risk_id="risk.001",
        actor_id="institution.alpha",
        exposure_amount=100,
        source_reference="credit.001",
        reason="credit exposure",
    )

    assert record.risk_id == "risk.001"
    assert record.actor_id == "institution.alpha"
    assert record.exposure_amount == 100
    assert record.source_reference == "credit.001"
    assert record.reason == "credit exposure"


def test_rejects_empty_risk_id():
    try:
        RiskRecord(
            risk_id="",
            actor_id="institution.alpha",
            exposure_amount=100,
            source_reference="credit.001",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "risk_id" in str(exc)


def test_rejects_non_positive_exposure():
    try:
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=0,
            source_reference="credit.001",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "exposure_amount" in str(exc)
