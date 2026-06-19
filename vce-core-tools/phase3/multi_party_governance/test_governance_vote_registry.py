from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)

from phase3.multi_party_governance.governance_vote_registry import (
    GovernanceVoteRegistry,
)


def test_registry_starts_empty():

    registry = GovernanceVoteRegistry()

    assert registry.count() == 0


def test_registry_accepts_vote():

    registry = GovernanceVoteRegistry()

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    registry.add(vote)

    assert registry.count() == 1


def test_registry_returns_vote():

    registry = GovernanceVoteRegistry()

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    registry.add(vote)

    recovered = registry.get(
        "vote-001"
    )

    assert recovered == vote


def test_missing_vote_returns_none():

    registry = GovernanceVoteRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_votes():

    registry = GovernanceVoteRegistry()

    vote1 = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    vote2 = GovernanceVoteRecord(
        vote_id="vote-002",
        voter_id="witness-002",
        vote="REJECT",
    )

    registry.add(vote1)
    registry.add(vote2)

    assert registry.vote_ids() == [
        "vote-001",
        "vote-002",
    ]
