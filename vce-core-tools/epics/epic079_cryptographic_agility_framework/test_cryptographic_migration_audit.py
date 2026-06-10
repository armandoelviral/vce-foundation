from epics.epic079_cryptographic_agility_framework.multi_signature_proof import (
    MultiSignatureProof,
    ProofSignature,
)

from epics.epic079_cryptographic_agility_framework.cryptographic_migration_audit import (
    CryptographicMigrationAudit,
)


def build_proofs():

    proof_1 = MultiSignatureProof(
        artifact_hash="artifact-001",
        signatures=[
            ProofSignature(
                signature_id="sig-001",
                algorithm_id="ecdsa-p256",
                signature_value="a",
                cryptographic_epoch="epoch-001",
            )
        ],
    )

    proof_2 = MultiSignatureProof(
        artifact_hash="artifact-002",
        signatures=[
            ProofSignature(
                signature_id="sig-002",
                algorithm_id="ml-dsa-65",
                signature_value="b",
                cryptographic_epoch="epoch-002",
            )
        ],
    )

    return [
        proof_1,
        proof_2,
    ]


def test_audit_counts_total_proofs():

    audit = CryptographicMigrationAudit(
        build_proofs()
    )

    assert audit.total_proofs() == 2


def test_audit_reports_algorithm_distribution():

    audit = CryptographicMigrationAudit(
        build_proofs()
    )

    report = audit.algorithm_distribution()

    assert report["ecdsa-p256"] == 1
    assert report["ml-dsa-65"] == 1


def test_audit_reports_epoch_distribution():

    audit = CryptographicMigrationAudit(
        build_proofs()
    )

    report = audit.epoch_distribution()

    assert report["epoch-001"] == 1
    assert report["epoch-002"] == 1


def test_audit_generates_migration_report():

    audit = CryptographicMigrationAudit(
        build_proofs()
    )

    report = audit.migration_report()

    assert report["total_proofs"] == 2

    assert (
        "algorithm_distribution"
        in report
    )

    assert (
        "epoch_distribution"
        in report
    )
