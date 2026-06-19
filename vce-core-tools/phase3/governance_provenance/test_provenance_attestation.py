from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)

from phase3.governance_provenance.provenance_attestation import (
    ProvenanceAttestation,
)


def test_attestation_subject():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    attestation = (
        ProvenanceAttestation.attest(
            attestation_id="att-001",
            record=record,
        )
    )

    assert (
        attestation.subject
        == "governance_provenance"
    )


def test_attestation_uses_provenance_id():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    attestation = (
        ProvenanceAttestation.attest(
            attestation_id="att-001",
            record=record,
        )
    )

    assert (
        attestation.evidence_hash
        == "prov-001"
    )


def test_attestation_preserves_id():

    record = GovernanceProvenanceRecord(
        provenance_id="prov-001",
        current_snapshot="snap-002",
        previous_snapshot="snap-001",
    )

    attestation = (
        ProvenanceAttestation.attest(
            attestation_id="att-001",
            record=record,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
