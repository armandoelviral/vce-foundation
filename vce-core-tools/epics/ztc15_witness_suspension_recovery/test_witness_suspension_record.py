from epics.ztc15_witness_suspension_recovery.witness_suspension_record import (
    WitnessSuspensionRecord,
)


def test_record_contains_witness_id():

    record = WitnessSuspensionRecord(
        witness_id="witness-001",
        reason="vote_divergence",
    )

    assert record.witness_id == "witness-001"


def test_record_contains_reason():

    record = WitnessSuspensionRecord(
        witness_id="witness-001",
        reason="vote_divergence",
    )

    assert record.reason == "vote_divergence"


def test_record_serializes():

    record = WitnessSuspensionRecord(
        witness_id="witness-001",
        reason="vote_divergence",
    )

    assert record.to_dict() == {
        "witness_id": "witness-001",
        "reason": "vote_divergence",
    }
