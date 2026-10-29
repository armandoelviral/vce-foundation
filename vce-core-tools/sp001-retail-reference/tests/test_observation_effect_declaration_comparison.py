"""SEC-MON-001 laboratory: committed content versus supplied declarations.

No production monitor, actor attribution, attempt counting or external anchor.
The observer trusts the destination database and its test-controlled baseline.
"""
import sqlite3
from contextlib import closing

import pytest

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture


def destination_snapshot(path):
    # Enumerate destination effects without taking identities from agent claims.
    uri = path.resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.execute("BEGIN")
        rows = connection.execute(
            "SELECT observation_id, observation_version, document "
            "FROM retail_inspection_observations"
        ).fetchall()
        connection.commit()
    return {(identity, version): document for identity, version, document in rows}


def compare_new_content(before, after, declared):
    # Test-only comparator. Existing rewrites/deletions are a separate anomaly.
    for identity, document in before.items():
        if after.get(identity) != document:
            raise ValueError("baseline changed or disappeared")
    new = {key: value for key, value in after.items() if key not in before}
    omitted = set(new) - set(declared)
    unsupported = set(declared) - set(new)
    contradictory = {
        key for key in set(new) & set(declared)
        if new[key] != declared[key]
    }
    return omitted, unsupported, contradictory


@pytest.mark.parametrize("declaration", ["omitted", "exact", "different"])
def test_destination_detects_omitted_or_contradictory_content(
    tmp_path, keys, declaration,
):
    path, service, _, _, _ = setup.environment(tmp_path, keys)
    before = destination_snapshot(path)
    item = setup.observation(case_id=setup.CASE)
    credential = jwt_setup.token(keys[0], operations=(setup.SAVE,))

    service.save(credential=credential, observation=item)

    after = destination_snapshot(path)
    identity = (item.observation_id, str(item.observation_version))
    assert identity not in before
    assert identity in after
    assert len(after) == len(before) + 1

    # Independently recover and validate the complete persisted document.
    from sp001.infrastructure.retail_inspection_observation_serialization import (
        deserialize_retail_inspection_observation as deserialize,
    )
    assert deserialize(after[identity]) == item

    declared = {}
    if declaration == "exact":
        declared[identity] = after[identity]
    elif declaration == "different":
        declared[identity] = "agent declares different content"

    omitted, unsupported, contradictory = compare_new_content(
        before, after, declared,
    )
    assert omitted == ({identity} if declaration == "omitted" else set())
    assert unsupported == set()
    assert contradictory == (
        {identity} if declaration == "different" else set()
    )

    # An exact retry produces no additional persisted content.
    service.save(credential=credential, observation=item)
    assert destination_snapshot(path) == after


def test_destination_failure_is_not_interpreted_as_no_activity(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        destination_snapshot(tmp_path / "missing.sqlite3")


def test_baseline_rewrite_or_deletion_is_not_silently_ignored():
    before = {("OBS", "1"): "original"}
    for after in ({}, {("OBS", "1"): "changed"}):
        with pytest.raises(ValueError, match="baseline"):
            compare_new_content(before, after, {})
