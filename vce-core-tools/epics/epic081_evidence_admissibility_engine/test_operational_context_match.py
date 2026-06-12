from epics.epic081_evidence_admissibility_engine.operational_context_match import (
    OperationalContextMatch,
)


def build_rule():

    return OperationalContextMatch()


def test_context_match_accepts_identical_contexts():

    rule = build_rule()

    expected = {
        "environment": "production",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    runtime = {
        "environment": "production",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    assert rule.matches(
        expected,
        runtime,
    ) is True


def test_context_match_rejects_environment_mismatch():

    rule = build_rule()

    expected = {
        "environment": "production",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    runtime = {
        "environment": "staging",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    assert rule.matches(
        expected,
        runtime,
    ) is False


def test_context_match_rejects_region_mismatch():

    rule = build_rule()

    expected = {
        "environment": "production",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    runtime = {
        "environment": "production",
        "region": "us-west-2",
        "process_id": "credit-risk-v7",
    }

    assert rule.matches(
        expected,
        runtime,
    ) is False


def test_context_match_rejects_missing_key():

    rule = build_rule()

    expected = {
        "environment": "production",
        "region": "us-east-1",
        "process_id": "credit-risk-v7",
    }

    runtime = {
        "environment": "production",
        "region": "us-east-1",
    }

    assert rule.matches(
        expected,
        runtime,
    ) is False
