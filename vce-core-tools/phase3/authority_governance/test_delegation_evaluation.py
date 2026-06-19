from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.delegation_evaluation import (
    DelegationEvaluation,
)


def test_governor_can_delegate():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    result = DelegationEvaluation.evaluate(
        authority
    )

    assert result is True


def test_auditor_cannot_delegate():

    authority = AuthorityRecord(
        authority_id="auth-002",
        principal_id="principal-002",
        role="AUDITOR",
    )

    result = DelegationEvaluation.evaluate(
        authority
    )

    assert result is False


def test_witness_cannot_delegate():

    authority = AuthorityRecord(
        authority_id="auth-003",
        principal_id="principal-003",
        role="WITNESS",
    )

    result = DelegationEvaluation.evaluate(
        authority
    )

    assert result is False
