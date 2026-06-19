from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)

from phase3.multi_party_governance.governance_vote_registry import (
    GovernanceVoteRegistry,
)

from phase3.multi_party_governance.governance_quorum_evaluation import (
    GovernanceQuorumEvaluation,
)

from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)

from phase3.multi_party_governance.governance_query import (
    GovernanceQuery,
)

from phase3.multi_party_governance.governance_report import (
    GovernanceReport,
)

from phase3.multi_party_governance.governance_attestation import (
    GovernanceAttestation,
)


def test_end_to_end_multi_party_governance():

    registry = GovernanceVoteRegistry()

    vote_1 = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    vote_2 = GovernanceVoteRecord(
        vote_id="vote-002",
        voter_id="witness-002",
        vote="APPROVE",
    )

    vote_3 = GovernanceVoteRecord(
        vote_id="vote-003",
        voter_id="witness-003",
        vote="REJECT",
    )

    registry.add(vote_1)
    registry.add(vote_2)
    registry.add(vote_3)

    votes = [
        registry.get("vote-001"),
        registry.get("vote-002"),
        registry.get("vote-003"),
    ]

    quorum = GovernanceQuorumEvaluation.evaluate(
        votes
    )

    assert quorum is True

    resolution = GovernanceResolution.from_quorum(
        quorum
    )

    assert resolution.status == "RESOLVED"

    resolutions = {
        "resolution-001": resolution
    }

    query = GovernanceQuery(
        resolutions
    )

    recovered = query.by_id(
        "resolution-001"
    )

    assert recovered == resolution

    report = GovernanceReport(
        resolutions
    )

    assert report.resolution_count() == 1
    assert report.resolution_ids() == [
        "resolution-001",
    ]

    attestation = GovernanceAttestation.attest(
        attestation_id="att-001",
        resolution=resolution,
    )

    assert attestation.subject == "governance_resolution"
    assert attestation.evidence_hash == "RESOLVED"
