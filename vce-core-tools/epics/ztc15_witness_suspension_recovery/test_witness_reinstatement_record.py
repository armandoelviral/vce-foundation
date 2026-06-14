from epics.ztc15_witness_suspension_recovery.witness_reinstatement_record import (
    WitnessReinstatementRecord,
)


def test_record_contains_witness_id():

    record = WitnessReinstatementRecord(
        witness_id="witness-001",
        reinstatement_reason="readmission_approved",
    )

    assert record.witness_id == "witness-001"


def test_record_contains_reason():

    record = WitnessReinstatementRecord(
        witness_id="witness-001",
        reinstatement_reason="readmission_approved",
    )

    assert record.reinstatement_reason == "readmission_approved"


def test_record_serializes():

    record = WitnessReinstatementRecord(
        witness_id="witness-001",
        reinstatement_reason="readmission_approved",
    )

    assert record.to_dict() == {
        "witness_id": "witness-001",
        "reinstatement_reason": "readmission_approved",
    }
