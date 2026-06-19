from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)

from phase3.governance_consensus_resolution.consensus_registry import (
    ConsensusRegistry,
)


def test_registry_starts_empty():

    registry = ConsensusRegistry()

    assert registry.count() == 0


def test_registry_accepts_record():

    registry = ConsensusRegistry()

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_returns_record():

    registry = ConsensusRegistry()

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    registry.add(record)

    recovered = registry.get(
        "consensus-001"
    )

    assert recovered == record


def test_missing_record_returns_none():

    registry = ConsensusRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_consensus_ids():

    registry = ConsensusRegistry()

    registry.add(
        ConsensusRecord(
            consensus_id="consensus-001",
            proposal_id="proposal-001",
            outcome="APPROVED",
        )
    )

    registry.add(
        ConsensusRecord(
            consensus_id="consensus-002",
            proposal_id="proposal-002",
            outcome="REJECTED",
        )
    )

    assert registry.consensus_ids() == [
        "consensus-001",
        "consensus-002",
    ]
