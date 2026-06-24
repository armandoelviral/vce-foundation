from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


def test_reserve_record_creation():
    record = ReserveRecord(
        reserve_id="reserve.001",
        institution_id="institution.alpha",
        reserve_amount=100,
        source_reference="capital.001",
    )

    assert record.reserve_id == "reserve.001"
    assert record.institution_id == "institution.alpha"
    assert record.reserve_amount == 100
    assert record.source_reference == "capital.001"


def test_rejects_empty_reserve_id():
    try:
        ReserveRecord(
            reserve_id="",
            institution_id="institution.alpha",
            reserve_amount=100,
            source_reference="capital.001",
        )
        assert False
    except ValueError as exc:
        assert "reserve_id" in str(exc)


def test_rejects_non_positive_reserve_amount():
    try:
        ReserveRecord(
            reserve_id="reserve.001",
            institution_id="institution.alpha",
            reserve_amount=0,
            source_reference="capital.001",
        )
        assert False
    except ValueError as exc:
        assert "reserve_amount" in str(exc)
