from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_report import (
    ProofReport,
)


def test_report_contains_proof_count():

    report = ProofReport(
        {
            "proof-001":
                InclusionProofRecord(
                    leaf_id="leaf-001",
                    root_id="root-001",
                    proof_hash="proof-hash-001",
                )
        }
    )

    assert report.proof_count() == 1


def test_report_lists_proof_ids():

    report = ProofReport(
        {
            "proof-001":
                InclusionProofRecord(
                    leaf_id="leaf-001",
                    root_id="root-001",
                    proof_hash="proof-hash-001",
                ),

            "proof-002":
                InclusionProofRecord(
                    leaf_id="leaf-002",
                    root_id="root-001",
                    proof_hash="proof-hash-002",
                ),
        }
    )

    assert report.proof_ids() == [
        "proof-001",
        "proof-002",
    ]


def test_report_serializes():

    report = ProofReport(
        {
            "proof-001":
                InclusionProofRecord(
                    leaf_id="leaf-001",
                    root_id="root-001",
                    proof_hash="proof-hash-001",
                )
        }
    )

    assert report.to_dict() == {
        "proof_count": 1,
        "proof_ids": [
            "proof-001",
        ],
    }
