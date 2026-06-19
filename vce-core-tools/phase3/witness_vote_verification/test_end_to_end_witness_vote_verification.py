from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_registry import (
    VoteRegistry,
)

from phase3.witness_vote_verification.vote_verification import (
    VoteVerification,
)

from phase3.witness_vote_verification.vote_decision import (
    VoteDecision,
)

from phase3.witness_vote_verification.vote_query import (
    VoteQuery,
)

from phase3.witness_vote_verification.vote_report import (
    VoteReport,
)

from phase3.witness_vote_verification.vote_attestation import (
    VoteAttestation,
)


def test_end_to_end_witness_vote_verification():

    registry = VoteRegistry()

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    registry.add(vote)

    verification = VoteVerification.verify(
        vote
    )

    assert verification is True

    decision = VoteDecision.from_verification(
        verification
    )

    assert (
        decision.status
        == "ACCEPT_VOTE"
    )

    query = VoteQuery(
        registry
    )

    recovered = query.by_id(
        "vote-001"
    )

    assert recovered == vote

    report = VoteReport(
        {
            "vote-001": recovered
        }
    )

    assert report.vote_count() == 1

    assert report.vote_ids() == [
        "vote-001"
    ]

    attestation = VoteAttestation.attest(
        attestation_id="att-001",
        vote=vote,
    )

    assert (
        attestation.subject
        == "witness_vote"
    )

    assert (
        attestation.evidence_hash
        == "vote-001"
    )
