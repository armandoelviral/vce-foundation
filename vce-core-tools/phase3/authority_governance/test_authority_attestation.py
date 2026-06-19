from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.authority_attestation import (
    AuthorityAttestation,
)


def test_attestation_subject():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    attestation = (
        AuthorityAttestation.attest(
            attestation_id="att-001",
            authority=authority,
        )
    )

    assert (
        attestation.subject
        == "authority_record"
    )


def test_attestation_uses_authority_id():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    attestation = (
        AuthorityAttestation.attest(
            attestation_id="att-001",
            authority=authority,
        )
    )

    assert (
        attestation.evidence_hash
        == "auth-001"
    )


def test_attestation_preserves_id():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    attestation = (
        AuthorityAttestation.attest(
            attestation_id="att-001",
            authority=authority,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
