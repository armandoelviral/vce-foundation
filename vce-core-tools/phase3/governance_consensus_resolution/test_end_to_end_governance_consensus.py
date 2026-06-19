from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)

from phase3.governance_consensus_resolution.consensus_registry import (
    ConsensusRegistry,
)

from phase3.governance_consensus_resolution.quorum_evaluation import (
    QuorumEvaluation,
)

from phase3.governance_consensus_resolution.majority_decision import (
    MajorityDecision,
)

from phase3.governance_consensus_resolution.consensus_query import (
    ConsensusQuery,
)

from phase3.governance_consensus_resolution.consensus_report import (
    ConsensusReport,
)

from phase3.governance_consensus_resolution.consensus_attestation import (
    ConsensusAttestation,
)


def test_end_to_end_governance_consensus():

    quorum = QuorumEvaluation.evaluate(
        vote_count=3
    )

    assert quorum is True

    outcome = MajorityDecision.decide(
        approve_votes=2,
        reject_votes=1,
    )

    assert outcome == "APPROVED"

    registry = ConsensusRegistry()

    consensus = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome=outcome,
    )

    registry.add(
        consensus
    )

    query = ConsensusQuery(
        registry
    )

    recovered = query.by_id(
        "consensus-001"
    )

    assert recovered == consensus

    report = ConsensusReport(
        {
            "consensus-001": recovered
        }
    )

    assert report.consensus_count() == 1

    assert report.consensus_ids() == [
        "consensus-001"
    ]

    attestation = (
        ConsensusAttestation.attest(
            attestation_id="att-001",
            consensus=consensus,
        )
    )

    assert (
        attestation.subject
        == "governance_consensus"
    )

    assert (
        attestation.evidence_hash
        == "consensus-001"
    )
