from phase2.witness_persistence.witness_vote_record import (
    WitnessVoteRecord,
)

from phase2.witness_persistence.witness_vote_store import (
    WitnessVoteStore,
)

from phase2.witness_persistence.witness_vote_query import (
    WitnessVoteQuery,
)

from phase2.witness_persistence.consensus_decision_record import (
    ConsensusDecisionRecord,
)

from phase2.witness_persistence.consensus_decision_verifier import (
    ConsensusDecisionVerifier,
)

from phase2.witness_persistence.witness_consensus_report import (
    WitnessConsensusReport,
)

from phase2.witness_persistence.witness_replay_binding import (
    WitnessReplayBinding,
)


def test_end_to_end_witness_persistence_flow():

    store = WitnessVoteStore()

    store.add(
        WitnessVoteRecord(
            witness_id="witness-001",
            decision_id="decision-001",
            vote=True,
        )
    )

    query = WitnessVoteQuery(store)

    votes = query.by_decision(
        "decision-001"
    )

    assert len(votes) == 1

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=len(votes),
    )

    verified = (
        ConsensusDecisionVerifier.verify(
            decision,
            required_votes=1,
        )
    )

    assert verified is True

    report = WitnessConsensusReport(
        [decision]
    )

    assert (
        report.total_decisions()
        == 1
    )

    binding = WitnessReplayBinding(
        decision_id="decision-001",
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100
