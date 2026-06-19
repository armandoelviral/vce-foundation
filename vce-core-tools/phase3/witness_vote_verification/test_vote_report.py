from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_report import (
    VoteReport,
)


def test_report_contains_vote_count():

    report = VoteReport(
        {
            "vote-001":
                WitnessVoteRecord(
                    vote_id="vote-001",
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    vote_value="APPROVE",
                )
        }
    )

    assert report.vote_count() == 1


def test_report_lists_vote_ids():

    report = VoteReport(
        {
            "vote-001":
                WitnessVoteRecord(
                    vote_id="vote-001",
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    vote_value="APPROVE",
                ),

            "vote-002":
                WitnessVoteRecord(
                    vote_id="vote-002",
                    witness_did="did:vcr:aws:us-east-1:fp002",
                    vote_value="REJECT",
                ),
        }
    )

    assert report.vote_ids() == [
        "vote-001",
        "vote-002",
    ]


def test_report_serializes():

    report = VoteReport(
        {
            "vote-001":
                WitnessVoteRecord(
                    vote_id="vote-001",
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    vote_value="APPROVE",
                )
        }
    )

    assert report.to_dict() == {
        "vote_count": 1,
        "vote_ids": [
            "vote-001",
        ],
    }
