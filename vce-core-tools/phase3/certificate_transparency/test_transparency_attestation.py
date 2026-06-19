from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_attestation import (
    TransparencyAttestation,
)


def test_attestation_subject():

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    attestation = (
        TransparencyAttestation.attest(
            attestation_id="att-001",
            entry=entry,
        )
    )

    assert (
        attestation.subject
        == "transparency_entry"
    )


def test_attestation_uses_entry_id():

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    attestation = (
        TransparencyAttestation.attest(
            attestation_id="att-001",
            entry=entry,
        )
    )

    assert (
        attestation.evidence_hash
        == "entry-001"
    )


def test_attestation_preserves_id():

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    attestation = (
        TransparencyAttestation.attest(
            attestation_id="att-001",
            entry=entry,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
