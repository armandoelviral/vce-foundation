from epics.epic043_snapshot_object.snapshot import Snapshot

from epics.epic049_state_provenance.provenance import (
    ProvenanceRecord,
)

from epics.epic051_signed_snapshot_attestation.signed_attestation import (
    SignedSnapshotAttestation,
)

from epics.epic055_runtime_proof.runtime_proof import (
    RuntimeProof,
)


def test_runtime_proof_aggregates_evidence():

    snapshot = Snapshot(
        sequence=42,
        state_hash="abc",
    )

    attestation = (
        SignedSnapshotAttestation(
            sequence=42,
            state_hash="abc",
            signature="sig",
        )
    )

    provenance = (
        ProvenanceRecord(
            snapshot_hash="abc",
            parent_hash=None,
        )
    )

    proof = RuntimeProof(
        snapshot=snapshot,
        attestation=attestation,
        provenance=provenance,
    )

    assert proof.snapshot == snapshot

    assert (
        proof.attestation
        == attestation
    )

    assert (
        proof.provenance
        == provenance
    )
