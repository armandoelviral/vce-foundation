from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
    RetailRuleEvaluationReportIdentity,
    RetailRuleEvaluationReportStore,
    StoredRetailRuleEvaluationReport,
)


def record(report_id="REPORT-1", document="synthetic opaque document"):
    return StoredRetailRuleEvaluationReport(
        RetailRuleEvaluationReportIdentity(report_id), document
    )


def test_preserves_exact_identity_and_document():
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    document = "  exact synthetic document\n"
    stored = StoredRetailRuleEvaluationReport(identity, document)
    assert stored.identity is identity
    assert stored.document == document


@pytest.mark.parametrize("value", ["", "  "])
def test_rejects_empty_identity(value):
    with pytest.raises(ValueError):
        RetailRuleEvaluationReportIdentity(value)


@pytest.mark.parametrize("value", [None, 1, True])
def test_rejects_invalid_identity_type(value):
    with pytest.raises(TypeError):
        RetailRuleEvaluationReportIdentity(value)


@pytest.mark.parametrize("value", ["", "  "])
def test_rejects_empty_document(value):
    with pytest.raises(ValueError):
        record(document=value)


@pytest.mark.parametrize("value", [None, b"document", 1])
def test_rejects_invalid_document_type(value):
    with pytest.raises(TypeError):
        record(document=value)


def test_rejects_non_nominal_identity():
    with pytest.raises(TypeError):
        StoredRetailRuleEvaluationReport("REPORT-1", "document")


def test_values_are_frozen():
    stored = record()
    with pytest.raises(FrozenInstanceError):
        stored.document = "replacement"
    with pytest.raises(FrozenInstanceError):
        stored.identity.report_id = "replacement"


class ReferenceStore:
    """Sequential test double; not a persistent or concurrent adapter."""

    def __init__(self):
        self.records = {}

    def put(self, *, report):
        previous = self.records.get(report.identity)
        if previous is not None:
            if previous.document != report.document:
                raise RetailRuleEvaluationReportConflict("identity conflict")
            return previous
        self.records[report.identity] = report
        return report

    def get(self, *, identity):
        return self.records.get(identity)


def test_reference_store_illustrates_idempotent_retry():
    store = ReferenceStore()
    assert isinstance(store, RetailRuleEvaluationReportStore)
    first = record()
    assert store.put(report=first) is first
    assert store.put(report=replace(first)) is first
    assert len(store.records) == 1


def test_reference_store_illustrates_conflict_without_replacement():
    store = ReferenceStore()
    first = record()
    store.put(report=first)
    with pytest.raises(RetailRuleEvaluationReportConflict):
        store.put(report=replace(first, document="contradictory document"))
    assert store.get(identity=first.identity) is first


def test_reference_store_preserves_separate_emissions():
    store = ReferenceStore()
    first = record("REPORT-1")
    second = record("REPORT-2")
    store.put(report=first)
    store.put(report=second)
    assert store.get(identity=first.identity) is first
    assert store.get(identity=second.identity) is second
    assert len(store.records) == 2


def test_reference_store_returns_none_only_for_absence():
    store = ReferenceStore()
    assert store.get(
        identity=RetailRuleEvaluationReportIdentity("ABSENT")
    ) is None
