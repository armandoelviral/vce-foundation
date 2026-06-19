from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)

from phase3.replay_revocation.revocation_submission import (
    RevocationSubmission,
)

from phase3.replay_revocation.revocation_verifier import (
    RevocationVerifier,
)

from phase3.replay_revocation.revocation_query import (
    RevocationQuery,
)

from phase3.replay_revocation.revocation_report import (
    RevocationReport,
)

from phase3.replay_revocation.revocation_attestation import (
    RevocationAttestation,
)


def test_end_to_end_replay_revocation():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry = RevocationRegistry()

    revocation = (
        RevocationSubmission.submit(
            revocation_id="rev-001",
            certificate=certificate,
            reason="key_compromise",
            registry=registry,
        )
    )

    assert (
        RevocationVerifier.is_revoked(
            registry,
            "cert-001",
        )
        is True
    )

    query = RevocationQuery(
        registry
    )

    recovered = query.by_id(
        "rev-001"
    )

    assert recovered == revocation

    report = RevocationReport(
        registry
    )

    assert (
        report.revocation_count()
        == 1
    )

    assert (
        report.revocation_ids()
        == ["rev-001"]
    )

    attestation = (
        RevocationAttestation.attest(
            attestation_id="att-001",
            revocation=revocation,
        )
    )

    assert (
        attestation.subject
        == "replay_revocation"
    )

    assert (
        attestation.evidence_hash
        == "rev-001"
    )
