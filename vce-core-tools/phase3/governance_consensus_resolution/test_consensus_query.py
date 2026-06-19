from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)

from phase3.governance_consensus_resolution.consensus_registry import (
    ConsensusRegistry,
)

from phase3.governance_consensus_resolution.consensus_query import (
    ConsensusQuery,
)


def test_query_returns_consensus():

    registry = ConsensusRegistry()

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    registry.add(record)

    query = ConsensusQuery(
        registry
    )

    result = query.by_id(
        "consensus-001"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = ConsensusRegistry()

    query = ConsensusQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_outcome():

    registry = ConsensusRegistry()

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    registry.add(record)

    query = ConsensusQuery(
        registry
    )

    result = query.by_id(
        "consensus-001"
    )

    assert result.outcome == "APPROVED"
