"""SEC-MON-001: separate observer process, trusted destination database.

Read-only SQLite connection, not OS-level isolation or a deployed monitor.
Only the database path is passed to the observer, never observation identities.
"""
import json
import os
import subprocess
import sys

import pytest

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_observation_effect_declaration_comparison import compare_new_content


OBSERVER = r"""
import json
import os
import sqlite3
import sys
from pathlib import Path

uri = Path(sys.argv[1]).resolve().as_uri() + "?mode=ro"
connection = sqlite3.connect(uri, uri=True)
try:
    connection.execute("BEGIN")
    rows = connection.execute(
        "SELECT observation_id, observation_version, document "
        "FROM retail_inspection_observations "
        "ORDER BY observation_id, observation_version"
    ).fetchall()
    connection.commit()
    try:
        connection.execute(
            "CREATE TABLE observer_write_probe (value TEXT)"
        )
    except sqlite3.OperationalError as error:
        if error.sqlite_errorcode & 255 != sqlite3.SQLITE_READONLY:
            raise
    else:
        raise AssertionError("observer connection allowed writing")
    print(json.dumps({
        "pid": os.getpid(),
        "write_rejected": True,
        "rows": rows,
    }))
finally:
    connection.close()
"""


def observe(path):
    result = subprocess.run(
        [sys.executable, "-c", OBSERVER, str(path)],
        capture_output=True,
        text=True,
        timeout=15,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["pid"] != os.getpid()
    assert payload["write_rejected"] is True
    rows = payload["rows"]
    snapshot = {
        (identity, version): document
        for identity, version, document in rows
    }
    assert len(snapshot) == len(rows)
    return snapshot


@pytest.mark.parametrize("declares_save", [False, True])
def test_separate_observer_discovers_effect_without_agent_identifiers(
    tmp_path, keys, declares_save,
):
    path, service, _, _, _ = setup.environment(tmp_path, keys)
    before = observe(path)
    assert before == {}

    item = setup.observation(case_id=setup.CASE)
    credential = jwt_setup.token(keys[0], operations=(setup.SAVE,))
    service.save(credential=credential, observation=item)

    after = observe(path)
    identity = (item.observation_id, str(item.observation_version))
    assert set(after) == {identity}

    from sp001.infrastructure.retail_inspection_observation_serialization import (
        serialize_retail_inspection_observation as serialize,
    )
    assert after[identity] == serialize(item)

    declared = {identity: serialize(item)} if declares_save else {}
    omitted, unsupported, contradictory = compare_new_content(
        before, after, declared,
    )
    assert omitted == (set() if declares_save else {identity})
    assert unsupported == set()
    assert contradictory == set()

    # Read-only probes and exact retry must leave destination content intact.
    service.save(credential=credential, observation=item)
    assert observe(path) == after


def test_separate_observer_failure_is_not_an_empty_snapshot(tmp_path):
    with pytest.raises(subprocess.CalledProcessError):
        observe(tmp_path / "missing.sqlite3")
    assert not (tmp_path / "missing.sqlite3").exists()
