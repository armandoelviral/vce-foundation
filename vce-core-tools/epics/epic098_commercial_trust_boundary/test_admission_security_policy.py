from epics.epic098_commercial_trust_boundary.admission_security_policy import (
    AdmissionSecurityPolicy,
)


def test_requires_mtls():

    policy = AdmissionSecurityPolicy(
        mtls_required=True,
        mldsa_required=True,
        admission_required=True,
    )

    assert policy.mtls_required is True


def test_requires_mldsa():

    policy = AdmissionSecurityPolicy(
        mtls_required=True,
        mldsa_required=True,
        admission_required=True,
    )

    assert policy.mldsa_required is True


def test_requires_admission():

    policy = AdmissionSecurityPolicy(
        mtls_required=True,
        mldsa_required=True,
        admission_required=True,
    )

    assert policy.admission_required is True


def test_serializes():

    policy = AdmissionSecurityPolicy(
        mtls_required=True,
        mldsa_required=True,
        admission_required=True,
    )

    assert policy.to_dict() == {
        "mtls_required": True,
        "mldsa_required": True,
        "admission_required": True,
    }
