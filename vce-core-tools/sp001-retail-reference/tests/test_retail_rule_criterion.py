from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_rule_criterion import RetailRuleCriterion


def test_preserves_exact_declared_criterion():
    statement = (
        "Synthetic example: viewed from the front, compare slots "
        "S1, S2 and S3 from left to right against blue, white and red. "
        "If any slot color cannot be established, evidence is insufficient."
    )
    criterion = RetailRuleCriterion("TEST-COLOR-001", 1, statement)

    assert criterion.rule_id == "TEST-COLOR-001"
    assert criterion.criterion_version == 1
    assert criterion.statement == statement


def test_criterion_is_frozen():
    criterion = RetailRuleCriterion("TEST-001", 1, "Declared criterion")
    with pytest.raises(FrozenInstanceError):
        criterion.statement = "Replacement"


def test_versions_preserve_distinct_content():
    first = RetailRuleCriterion("TEST-001", 1, "Original criterion")
    second = RetailRuleCriterion("TEST-001", 2, "Revised criterion")

    assert first != second
    assert first.statement == "Original criterion"


@pytest.mark.parametrize("field", ["rule_id", "statement"])
@pytest.mark.parametrize("value", ["", "   "])
def test_rejects_empty_text(field, value):
    values = dict(
        rule_id="TEST-001", criterion_version=1, statement="Criterion"
    )
    values[field] = value
    with pytest.raises(ValueError):
        RetailRuleCriterion(**values)


@pytest.mark.parametrize("field", ["rule_id", "statement"])
@pytest.mark.parametrize("value", [None, 42])
def test_rejects_non_string_text(field, value):
    values = dict(
        rule_id="TEST-001", criterion_version=1, statement="Criterion"
    )
    values[field] = value
    with pytest.raises(TypeError):
        RetailRuleCriterion(**values)


@pytest.mark.parametrize("version", [True, False, 1.0, "1", None])
def test_rejects_non_integer_version(version):
    with pytest.raises(TypeError):
        RetailRuleCriterion("TEST-001", version, "Criterion")


@pytest.mark.parametrize("version", [0, -1])
def test_rejects_non_positive_version(version):
    with pytest.raises(ValueError):
        RetailRuleCriterion("TEST-001", version, "Criterion")
