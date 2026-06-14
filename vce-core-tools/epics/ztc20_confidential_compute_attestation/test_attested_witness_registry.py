from epics.ztc20_confidential_compute_attestation.attestation_admission_record import (
    AttestationAdmissionRecord,
)

from epics.ztc20_confidential_compute_attestation.attested_witness_registry import (
    AttestedWitnessRegistry,
)


def test_registry_stores_admitted_witness():

    registry = AttestedWitnessRegistry()

    record = AttestationAdmissionRecord(
        witness_id="witness-001",
        admitted=True,
        reason="attestation_verified",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_reports_attested_witness():

    registry = AttestedWitnessRegistry()

    registry.add(
        AttestationAdmissionRecord(
            witness_id="witness-001",
            admitted=True,
            reason="attestation_verified",
        )
    )

    assert registry.is_attested(
        "witness-001"
    )


def test_registry_returns_false_for_unknown_witness():

    registry = AttestedWitnessRegistry()

    assert not registry.is_attested(
        "witness-999"
    )
