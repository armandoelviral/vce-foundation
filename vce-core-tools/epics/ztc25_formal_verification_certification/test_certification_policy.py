from epics.ztc25_formal_verification_certification.certification_policy import (
    CertificationPolicy,
)


def test_accepts_validated_system():

    policy = CertificationPolicy()

    assert policy.certify(
        safety_properties_validated=True,
    )


def test_rejects_unvalidated_system():

    policy = CertificationPolicy()

    assert not policy.certify(
        safety_properties_validated=False,
    )


def test_returns_boolean():

    policy = CertificationPolicy()

    result = policy.certify(
        safety_properties_validated=True,
    )

    assert isinstance(
        result,
        bool,
    )
