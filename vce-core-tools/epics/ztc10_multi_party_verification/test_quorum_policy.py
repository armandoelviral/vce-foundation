from epics.ztc10_multi_party_verification.quorum_policy import (
    QuorumPolicy,
)


def test_accepts_root_meeting_quorum():

    ballot = {
        "root-a": ["w1", "w2"],
        "root-b": ["w3"],
    }

    winner = QuorumPolicy.select(
        ballot,
        minimum_witnesses=2,
    )

    assert winner == "root-a"


def test_returns_none_when_quorum_not_reached():

    ballot = {
        "root-a": ["w1"],
        "root-b": ["w2"],
        "root-c": ["w3"],
    }

    winner = QuorumPolicy.select(
        ballot,
        minimum_witnesses=2,
    )

    assert winner is None


def test_accepts_larger_quorum():

    ballot = {
        "root-a": ["w1", "w2", "w3"],
        "root-b": ["w4"],
    }

    winner = QuorumPolicy.select(
        ballot,
        minimum_witnesses=3,
    )

    assert winner == "root-a"
