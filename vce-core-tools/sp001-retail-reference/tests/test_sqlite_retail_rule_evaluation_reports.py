import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
    RetailRuleEvaluationReportIdentity,
    RetailRuleEvaluationReportStore,
    StoredRetailRuleEvaluationReport,
)
from sp001.infrastructure.sqlite_retail_rule_evaluation_reports import (
    SqliteRetailRuleEvaluationReportStore,
)


def record(identity="REPORT-1", document="synthetic opaque document"):
    return StoredRetailRuleEvaluationReport(
        RetailRuleEvaluationReportIdentity(identity), document
    )


def test_reopens_and_recovers_exact_document(tmp_path):
    path = tmp_path / "reports.sqlite3"
    store = SqliteRetailRuleEvaluationReportStore(database_path=path)
    assert isinstance(store, RetailRuleEvaluationReportStore)
    original = record(document="  exact synthetic text\n")
    assert store.put(report=original) == original

    reopened = SqliteRetailRuleEvaluationReportStore(database_path=path)
    assert reopened.get(identity=original.identity) == original


def test_identical_retry_keeps_one_row(tmp_path):
    path = tmp_path / "reports.sqlite3"
    store = SqliteRetailRuleEvaluationReportStore(database_path=path)
    original = record()
    assert store.put(report=original) == original
    assert store.put(report=record()) == original
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0] == 1


def test_conflict_preserves_original_and_allows_fresh_emission(tmp_path):
    store = SqliteRetailRuleEvaluationReportStore(
        database_path=tmp_path / "reports.sqlite3"
    )
    original = record()
    store.put(report=original)
    with pytest.raises(RetailRuleEvaluationReportConflict):
        store.put(report=record(document="contradictory text"))

    assert store.get(identity=original.identity) == original
    fresh = record("REPORT-2", "contradictory text")
    assert store.put(report=fresh) == fresh
    assert store.get(identity=original.identity) == original
    assert store.get(identity=fresh.identity) == fresh


def test_absence_is_none(tmp_path):
    store = SqliteRetailRuleEvaluationReportStore(
        database_path=tmp_path / "reports.sqlite3"
    )
    assert store.get(
        identity=RetailRuleEvaluationReportIdentity("ABSENT")
    ) is None


@pytest.mark.parametrize("contradictory", [False, True])
def test_race_between_independent_connections(tmp_path, contradictory):
    path = tmp_path / "reports.sqlite3"
    stores = [
        SqliteRetailRuleEvaluationReportStore(database_path=path)
        for _ in range(2)
    ]
    barrier = Barrier(2)
    submissions = [
        record(document="first document"),
        record(document=(
            "second document" if contradictory else "first document"
        )),
    ]

    def attempt(index):
        barrier.wait(timeout=5)
        try:
            return ("confirmed", stores[index].put(report=submissions[index]))
        except RetailRuleEvaluationReportConflict:
            return ("conflict", None)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(attempt, range(2)))

    confirmed = [value for status, value in results if status == "confirmed"]
    conflicts = [status for status, _ in results if status == "conflict"]
    assert len(confirmed) == (1 if contradictory else 2)
    assert len(conflicts) == (1 if contradictory else 0)

    reopened = SqliteRetailRuleEvaluationReportStore(database_path=path)
    winner = reopened.get(identity=submissions[0].identity)
    assert winner == confirmed[0]
    assert all(value == winner for value in confirmed)

    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0] == 1


def test_backend_failure_is_not_absence(tmp_path):
    path = tmp_path / "reports.sqlite3"
    store = SqliteRetailRuleEvaluationReportStore(database_path=path)
    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE retail_rule_evaluation_reports")

    with pytest.raises(sqlite3.OperationalError):
        store.get(identity=RetailRuleEvaluationReportIdentity("REPORT-1"))
    with pytest.raises(sqlite3.OperationalError):
        store.put(report=record())


@pytest.mark.parametrize("value", [None, "REPORT-1"])
def test_rejects_invalid_get_identity(tmp_path, value):
    store = SqliteRetailRuleEvaluationReportStore(
        database_path=tmp_path / "reports.sqlite3"
    )
    with pytest.raises(TypeError):
        store.get(identity=value)


def test_rejects_invalid_put_record(tmp_path):
    store = SqliteRetailRuleEvaluationReportStore(
        database_path=tmp_path / "reports.sqlite3"
    )
    with pytest.raises(TypeError):
        store.put(report="document")


@pytest.mark.parametrize("value", ["", " ", ":memory:"])
def test_rejects_non_file_database_configuration(value):
    with pytest.raises(ValueError):
        SqliteRetailRuleEvaluationReportStore(database_path=value)
