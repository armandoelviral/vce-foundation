from epics.ztc25_formal_verification_certification.formal_invariant import (
    FormalInvariant,
)

from epics.ztc25_formal_verification_certification.invariant_registry import (
    InvariantRegistry,
)

from epics.ztc25_formal_verification_certification.proof_obligation import (
    ProofObligation,
)

from epics.ztc25_formal_verification_certification.safety_property_validator import (
    SafetyPropertyValidator,
)

from epics.ztc25_formal_verification_certification.certification_policy import (
    CertificationPolicy,
)

from epics.ztc25_formal_verification_certification.certification_record import (
    CertificationRecord,
)

from epics.ztc25_formal_verification_certification.certification_report import (
    CertificationReport,
)


def test_end_to_end_formal_verification_certification_flow():

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    registry = InvariantRegistry()

    registry.add(
        invariant
    )

    assert registry.exists(
        "INV-001"
    )

    obligation = ProofObligation(
        obligation_id="PO-001",
        invariant_id="INV-001",
        description="prove sequence monotonicity",
    )

    assert obligation.invariant_id == "INV-001"

    validator = SafetyPropertyValidator()

    safety_valid = validator.validate(
        property_satisfied=True,
    )

    assert safety_valid is True

    policy = CertificationPolicy()

    certified = policy.certify(
        safety_properties_validated=safety_valid,
    )

    assert certified is True

    record = CertificationRecord(
        certification_id="cert-001",
        certified=certified,
        reason="all_safety_properties_validated",
    )

    assert record.certified is True

    report = CertificationReport(
        report_id="report-001",
        obligations_checked=1,
        violations=0,
    )

    assert report.satisfied() == 1
