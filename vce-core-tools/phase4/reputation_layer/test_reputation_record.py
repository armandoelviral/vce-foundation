from phase4.reputation_layer.reputation_record import (
    ReputationRecord,
)


def test_contains_did():

    record = ReputationRecord(
        citizen_did="did:tcn:test:01",
        reputation_score=100,
    )

    assert record.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_score():

    record = ReputationRecord(
        citizen_did="did:tcn:test:01",
        reputation_score=100,
    )

    assert record.reputation_score == 100


def test_serializes():

    record = ReputationRecord(
        citizen_did="did:tcn:test:01",
        reputation_score=100,
    )

    assert record.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "reputation_score": 100,
    }
