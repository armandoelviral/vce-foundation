from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_report import (
    SignatureReport,
)


def test_report_contains_signature_count():

    report = SignatureReport(
        {
            "sig-001":
                HybridSignatureRecord(
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    classical_signature="ed25519-sig",
                    pqc_signature="mldsa-sig",
                )
        }
    )

    assert report.signature_count() == 1


def test_report_lists_signature_ids():

    report = SignatureReport(
        {
            "sig-001":
                HybridSignatureRecord(
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    classical_signature="ed25519-sig",
                    pqc_signature="mldsa-sig",
                ),

            "sig-002":
                HybridSignatureRecord(
                    witness_did="did:vcr:aws:us-east-1:fp002",
                    classical_signature="ed25519-sig-2",
                    pqc_signature="mldsa-sig-2",
                ),
        }
    )

    assert report.signature_ids() == [
        "sig-001",
        "sig-002",
    ]


def test_report_serializes():

    report = SignatureReport(
        {
            "sig-001":
                HybridSignatureRecord(
                    witness_did="did:vcr:gcp:us-central1:fp001",
                    classical_signature="ed25519-sig",
                    pqc_signature="mldsa-sig",
                )
        }
    )

    assert report.to_dict() == {
        "signature_count": 1,
        "signature_ids": [
            "sig-001",
        ],
    }
