from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)

from epics.ztc20_confidential_compute_attestation.attestation_registry import (
    AttestationRegistry,
)


def test_registry_stores_attestation():

    registry = AttestationRegistry()

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    registry.add(evidence)

    assert registry.count() == 1


def test_registry_returns_attestation():

    registry = AttestationRegistry()

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    registry.add(evidence)

    records = registry.all()

    assert len(records) == 1
    assert records[0].witness_id == "witness-001"


def test_registry_starts_empty():

    registry = AttestationRegistry()

    assert registry.count() == 0


def test_registry_supports_multiple_providers():

    registry = AttestationRegistry()

    registry.add(
        AttestationEvidence(
            witness_id="witness-aws",
            provider="aws",
            evidence_hash="hash-001",
        )
    )

    registry.add(
        AttestationEvidence(
            witness_id="witness-gcp",
            provider="gcp",
            evidence_hash="hash-002",
        )
    )

    registry.add(
        AttestationEvidence(
            witness_id="witness-azure",
            provider="azure",
            evidence_hash="hash-003",
        )
    )

    assert registry.count() == 3
