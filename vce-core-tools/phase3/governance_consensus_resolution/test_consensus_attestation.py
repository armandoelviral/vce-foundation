from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)

from phase3.governance_consensus_resolution.consensus_attestation import (
    ConsensusAttestation,
)


def test_attestation_subject():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    attestation = ConsensusAttestation.attest(
        attestation_id="att-001",
        consensus=record,
    )

    assert attestation.subject == "governance_consensus"


def test_attestation_uses_consensus_id():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    attestation = ConsensusAttestation.attest(
        attestation_id="att-001",
        consensus=record,
    )

    assert attestation.evidence_hash == "consensus-001"


def test_attestation_preserves_id():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    attestation = ConsensusAttestation.attest(
        attestation_id="att-001",
        consensus=record,
    )

    assert attestation.attestation_id == "att-001"
