from epics.epic086_historical_policy_replay_audit.witness_replay_vote import (
    WitnessReplayVote,
)


def build_vote(
    replay_result="REPLAY_MATCH",
):

    return WitnessReplayVote(
        witness_id="witness-001",
        evidence_hash="evidence-hash-001",
        policy_id="clinical-admission-policy",
        policy_version="2.0.0",
        replay_result=replay_result,
        observed_at="2026-06-10T00:00:00Z",
    )


def test_witness_replay_vote_creation():

    vote = build_vote()

    assert vote.witness_id == "witness-001"
    assert vote.evidence_hash == "evidence-hash-001"
    assert vote.replay_result == "REPLAY_MATCH"


def test_witness_replay_vote_contains_policy_version():

    vote = build_vote()

    assert vote.policy_id == "clinical-admission-policy"
    assert vote.policy_version == "2.0.0"


def test_witness_replay_vote_can_record_mismatch():

    vote = build_vote(
        replay_result="REPLAY_MISMATCH"
    )

    assert vote.replay_result == "REPLAY_MISMATCH"


def test_witness_replay_vote_serializes():

    vote = build_vote()

    payload = vote.to_dict()

    assert payload["witness_id"] == "witness-001"
    assert payload["evidence_hash"] == "evidence-hash-001"
    assert payload["policy_version"] == "2.0.0"
