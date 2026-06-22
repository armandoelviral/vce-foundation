from phase4.response_validity_layer.response_evidence import (
    ResponseEvidence,
)


def test_contains_did():

    evidence = ResponseEvidence(
        citizen_did="did:tcn:test:01",
        evidence_type="heartbeat",
        evidence_value="alive",
    )

    assert evidence.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_type():

    evidence = ResponseEvidence(
        citizen_did="did:tcn:test:01",
        evidence_type="heartbeat",
        evidence_value="alive",
    )

    assert evidence.evidence_type == (
        "heartbeat"
    )


def test_contains_value():

    evidence = ResponseEvidence(
        citizen_did="did:tcn:test:01",
        evidence_type="heartbeat",
        evidence_value="alive",
    )

    assert evidence.evidence_value == (
        "alive"
    )


def test_serializes():

    evidence = ResponseEvidence(
        citizen_did="did:tcn:test:01",
        evidence_type="heartbeat",
        evidence_value="alive",
    )

    assert evidence.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "evidence_type": "heartbeat",
        "evidence_value": "alive",
    }
