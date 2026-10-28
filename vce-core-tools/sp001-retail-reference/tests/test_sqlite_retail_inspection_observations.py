import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
    RetailInspectionObservationIdentity as Identity,
    RetailInspectionObservationStore,
    StoredRetailInspectionObservation as Stored,
)
from sp001.infrastructure.sqlite_retail_inspection_observations import (
    SqliteRetailInspectionObservationStore as Store,
)


def record(observation_id="OBS", version=1, document="opaque document"):
    return Stored(Identity(observation_id, version), document)


def count(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM retail_inspection_observations"
        ).fetchone()[0]


def test_reopens_and_preserves_exact_document(tmp_path):
    path = tmp_path / "observations.sqlite3"
    store = Store(database_path=path)
    assert isinstance(store, RetailInspectionObservationStore)
    original = record(document="  Texto exacto: á\n")
    assert store.put(observation=original) == original
    assert Store(database_path=path).get(identity=original.identity) == original


def test_identical_retry_keeps_one_record(tmp_path):
    path = tmp_path / "observations.sqlite3"
    store = Store(database_path=path)
    original = record()
    assert store.put(observation=original) == original
    assert store.put(observation=record()) == original
    assert count(path) == 1


def test_conflict_preserves_original_and_allows_new_version(tmp_path):
    path = tmp_path / "observations.sqlite3"
    store = Store(database_path=path)
    original = record()
    store.put(observation=original)
    with pytest.raises(Conflict):
        store.put(observation=record(document="contradictory"))
    assert store.get(identity=original.identity) == original
    assert count(path) == 1
    revised = record(version=2, document="corrected")
    store.put(observation=revised)
    reopened = Store(database_path=path)
    assert reopened.get(identity=original.identity) == original
    assert reopened.get(identity=revised.identity) == revised
    assert count(path) == 2


def test_versions_are_independent_and_exact_absence_is_none(tmp_path):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    for item in (record(version=7), record(version=2), record("OTHER", 2)):
        store.put(observation=item)
        assert store.get(identity=item.identity) == item
    assert store.get(identity=Identity("OBS", 1)) is None
    assert store.get(identity=Identity("MISSING", 2)) is None


def test_supports_positive_versions_beyond_sqlite_integer_range(tmp_path):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    original = record(version=2**80)
    assert store.put(observation=original) == original
    assert store.get(identity=original.identity) == original


@pytest.mark.parametrize("scenario", ["identical", "conflict", "versions"])
def test_two_connection_race(tmp_path, scenario):
    path = tmp_path / "observations.sqlite3"
    stores = [Store(database_path=path), Store(database_path=path)]
    first = record(document="first")
    second = record(
        version=2 if scenario == "versions" else 1,
        document="first" if scenario == "identical" else "second",
    )
    submissions = [first, second]
    barrier = Barrier(2)

    def attempt(index):
        barrier.wait(timeout=5)
        try:
            return ("confirmed", stores[index].put(
                observation=submissions[index],
            ))
        except Conflict:
            return ("conflict", None)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(attempt, range(2)))

    confirmed = [item for status, item in results if status == "confirmed"]
    conflicts = [status for status, _ in results if status == "conflict"]
    assert len(confirmed) == (1 if scenario == "conflict" else 2)
    assert len(conflicts) == (1 if scenario == "conflict" else 0)
    reopened = Store(database_path=path)
    for item in confirmed:
        assert reopened.get(identity=item.identity) == item
    assert count(path) == (2 if scenario == "versions" else 1)
    if scenario == "conflict":
        assert confirmed[0] in submissions
        winner = reopened.get(identity=first.identity)
        assert winner == confirmed[0]
        loser = second if winner == first else first
        with pytest.raises(Conflict):
            reopened.put(observation=loser)
        assert reopened.get(identity=winner.identity) == winner


def test_backend_failure_is_not_absence(tmp_path):
    path = tmp_path / "observations.sqlite3"
    store = Store(database_path=path)
    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE retail_inspection_observations")
    with pytest.raises(sqlite3.OperationalError):
        store.get(identity=Identity("OBS", 1))
    with pytest.raises(sqlite3.OperationalError):
        store.put(observation=record())


@pytest.mark.parametrize("value", [None, "OBS", ("OBS", 1)])
def test_rejects_invalid_get_identity(tmp_path, value):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    with pytest.raises(TypeError):
        store.get(identity=value)


@pytest.mark.parametrize("value", [None, "document"])
def test_rejects_invalid_put_record(tmp_path, value):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    with pytest.raises(TypeError):
        store.put(observation=value)


@pytest.mark.parametrize("value", ["", " ", ":memory:"])
def test_rejects_non_file_configuration(value):
    with pytest.raises(ValueError):
        Store(database_path=value)


def test_rejects_invalid_database_path_type():
    with pytest.raises(TypeError):
        Store(database_path=1)
