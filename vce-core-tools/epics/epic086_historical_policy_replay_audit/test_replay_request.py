from epics.epic086_historical_policy_replay_audit.replay_request import (
    ReplayRequest,
)


def build_request():

    return ReplayRequest(
        evidence_hash="evidence-hash-001",
        policy_id="clinical-admission-policy",
        policy_version="2.0.0",
        requested_by="external-auditor",
        requested_at="2026-06-10T00:00:00Z",
    )


def test_replay_request_creation():

    request = build_request()

    assert (
        request.evidence_hash
        == "evidence-hash-001"
    )

    assert (
        request.policy_id
        == "clinical-admission-policy"
    )


def test_replay_request_contains_policy_version():

    request = build_request()

    assert (
        request.policy_version
        == "2.0.0"
    )


def test_replay_request_contains_auditor():

    request = build_request()

    assert (
        request.requested_by
        == "external-auditor"
    )


def test_replay_request_serializes():

    request = build_request()

    payload = request.to_dict()

    assert (
        payload["evidence_hash"]
        == "evidence-hash-001"
    )

    assert (
        payload["policy_version"]
        == "2.0.0"
    )

    assert (
        payload["requested_by"]
        == "external-auditor"
    )
