from epics.epic081_evidence_admissibility_engine.cps_threshold_rule import (
    CPSThresholdRule,
)


def build_rule():

    return CPSThresholdRule()


def test_rule_accepts_equal_threshold():

    rule = build_rule()

    assert (
        rule.is_satisfied(
            artifact_cps=5,
            required_cps=5,
        )
        is True
    )


def test_rule_accepts_higher_threshold():

    rule = build_rule()

    assert (
        rule.is_satisfied(
            artifact_cps=5,
            required_cps=4,
        )
        is True
    )


def test_rule_rejects_lower_threshold():

    rule = build_rule()

    assert (
        rule.is_satisfied(
            artifact_cps=3,
            required_cps=5,
        )
        is False
    )


def test_rule_supports_financial_policy():

    rule = build_rule()

    assert (
        rule.is_satisfied(
            artifact_cps=4,
            required_cps=4,
        )
        is True
    )


def test_rule_supports_analytics_policy():

    rule = build_rule()

    assert (
        rule.is_satisfied(
            artifact_cps=2,
            required_cps=2,
        )
        is True
    )
