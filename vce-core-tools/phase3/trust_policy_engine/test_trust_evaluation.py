from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)

from phase3.trust_policy_engine.trust_evaluation import (
    TrustEvaluation,
)


def test_valid_certificate_passes():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    result = TrustEvaluation.evaluate(
        policy=policy,
        certificate_exists=True,
        certificate_published=True,
        certificate_revoked=False,
    )

    assert result is True


def test_missing_certificate_fails():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    result = TrustEvaluation.evaluate(
        policy=policy,
        certificate_exists=False,
        certificate_published=True,
        certificate_revoked=False,
    )

    assert result is False


def test_revoked_certificate_fails():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    result = TrustEvaluation.evaluate(
        policy=policy,
        certificate_exists=True,
        certificate_published=True,
        certificate_revoked=True,
    )

    assert result is False


def test_unpublished_certificate_fails():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    result = TrustEvaluation.evaluate(
        policy=policy,
        certificate_exists=True,
        certificate_published=False,
        certificate_revoked=False,
    )

    assert result is False
