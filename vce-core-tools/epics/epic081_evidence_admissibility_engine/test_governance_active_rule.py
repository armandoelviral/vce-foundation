from epics.epic081_evidence_admissibility_engine.governance_active_rule import (
    GovernanceActiveRule,
)


def test_governance_active_rule_accepts_active_status():

    rule = GovernanceActiveRule()

    assert rule.is_active(
        "ACTIVE"
    ) is True


def test_governance_active_rule_rejects_revoked_status():

    rule = GovernanceActiveRule()

    assert rule.is_active(
        "REVOKED"
    ) is False


def test_governance_active_rule_rejects_expired_status():

    rule = GovernanceActiveRule()

    assert rule.is_active(
        "EXPIRED"
    ) is False


def test_governance_active_rule_rejects_missing_status():

    rule = GovernanceActiveRule()

    assert rule.is_active(
        None
    ) is False
