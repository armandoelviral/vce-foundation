import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys

import pytest

import test_retail_report_attribution_admission as setup


CHILD = r"""
import json
import os
from pathlib import Path
import signal
import sqlite3
import sys

root = Path.cwd()
sys.path.insert(0, str(root / "src"))
sys.path.insert(0, str(root / "tests"))

import test_retail_report_attribution_admission as setup

directory = Path(sys.argv[1])
mode = sys.argv[2]
(
    path, _, _, report, _, _, _, _, _, backend, service,
) = setup.environment(directory)
real_connect = sqlite3.connect


class CrashConnection(sqlite3.Connection):
    def execute(self, sql, parameters=()):
        if sql.strip().upper() != "COMMIT":
            return super().execute(sql, parameters)

        # Both writes must exist inside this transaction before interruption.
        reports = super().execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0]
        admissions = super().execute(
            "SELECT COUNT(*) FROM retail_evaluation_admissions"
        ).fetchone()[0]
        if (reports, admissions) != (1, 1) or not self.in_transaction:
            raise AssertionError("unexpected pre-commit state")

        if mode == "after":
            result = super().execute(sql, parameters)
            if self.in_transaction:
                raise AssertionError("commit did not end the transaction")
        elif mode != "before":
            raise AssertionError("unknown crash position")

        print(json.dumps({
            "position": mode,
            "reports_inside_transaction": reports,
            "admissions_inside_transaction": admissions,
            "transaction_active_at_kill": self.in_transaction,
        }), flush=True)
        os.kill(os.getpid(), signal.SIGKILL)
        raise AssertionError("SIGKILL did not terminate the process")


def connect():
    connection = real_connect(
        path, timeout=5.0, isolation_level=None, factory=CrashConnection,
    )
    connection.execute("PRAGMA synchronous=FULL")
    return connection


backend._connect = connect
setup.save(service, report)
raise AssertionError("save unexpectedly returned")
"""


def persisted_documents(path):
    with sqlite3.connect(path) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        reports = connection.execute(
            "SELECT report_id, document "
            "FROM retail_rule_evaluation_reports ORDER BY report_id"
        ).fetchall()
        admissions = connection.execute(
            "SELECT evaluation_id, document "
            "FROM retail_evaluation_admissions ORDER BY evaluation_id"
        ).fetchall()
    return reports, admissions


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX SIGKILL")
@pytest.mark.parametrize("position", ["before", "after"])
def test_process_crash_preserves_atomicity_and_idempotent_recovery(
    tmp_path, position,
):
    (
        path, _, _, report, _, _, _, _, _, _, _,
    ) = setup.environment(tmp_path)
    assert setup.counts(path) == (0, 0)

    root = Path(__file__).resolve().parents[1]
    child = subprocess.run(
        [sys.executable, "-c", CHILD, str(tmp_path), position],
        cwd=root, capture_output=True, text=True, timeout=30,
    )
    assert child.returncode == -signal.SIGKILL, (
        child.returncode, child.stdout, child.stderr,
    )
    marker = json.loads(child.stdout)
    assert marker == {
        "position": position,
        "reports_inside_transaction": 1,
        "admissions_inside_transaction": 1,
        "transaction_active_at_kill": position == "before",
    }

    # Inspect using a fresh connection after the child has died.
    persisted = persisted_documents(path)
    expected_count = 0 if position == "before" else 1
    assert tuple(map(len, persisted)) == (expected_count, expected_count)

    # Reconstruct application components, not merely the SQLite connection.
    (
        reopened_path, _, _, reopened_report, _, bindings,
        _, _, auth, _, service,
    ) = setup.environment(tmp_path)
    assert reopened_path == path
    assert reopened_report == report
    assert len(bindings.read_history(binding_id="BINDING")) == 1

    recovered = service.recover(
        credential="valid", identity=setup.Identity("REPORT"), case_id="CASE",
    )
    if position == "before":
        assert recovered is None
        assert setup.save(service, report) == report
    else:
        assert recovered == report
        assert setup.save(service, report, references=()) == report
        assert persisted_documents(path) == persisted

    confirmed = persisted_documents(path)
    assert tuple(map(len, confirmed)) == (1, 1)

    # Another authorized retry must preserve both documents exactly.
    assert setup.save(service, report, references=()) == report
    assert persisted_documents(path) == confirmed
    assert setup.counts(path) == (1, 1)
    assert auth.calls == 3
