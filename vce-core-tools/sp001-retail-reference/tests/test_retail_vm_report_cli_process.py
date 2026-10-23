import os
from pathlib import Path
import subprocess
import sys

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import test_retail_report_jwt_composition as setup
import test_retail_vm_report_cli as cli_setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)


@pytest.fixture(scope="module")
def process_keys():
    # Synthetic keys generated only within tests.
    return tuple(
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        for _ in range(2)
    )


def execute_cli(path, keys, credential, destination, *, report_id="REPORT-1",
                include_key=True):
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root / "src")
    environment.pop("VM_TEST_PUBLIC_KEY", None)
    if include_key:
        environment["VM_TEST_PUBLIC_KEY"] = (
            keys[0].public_key().public_bytes(
                Encoding.PEM, PublicFormat.SubjectPublicKeyInfo,
            ).decode("ascii")
        )
    command = [
        sys.executable, "-m", "sp001.infrastructure.retail_vm_report_cli",
        *cli_setup.arguments(path, report_id=report_id),
    ]
    assert credential not in command
    with destination.open("xb") as output:
        completed = subprocess.run(
            command, input=(credential + "\n").encode("ascii"),
            stdout=output, stderr=subprocess.PIPE,
            cwd=root, env=environment, timeout=30,
        )
    return (
        completed.returncode,
        destination.read_text(encoding="utf-8"),
        completed.stderr.decode("utf-8"),
    )


def save_report(service, credential):
    report = setup.make_report()
    service.save(
        credential=credential, identity=setup.IDENTITY, report=report,
    )
    return report


def test_process_exports_readable_authorized_report(tmp_path, process_keys):
    path, service, _, _ = setup.environment(tmp_path, process_keys)
    credential = setup.token(process_keys[0])
    report = save_report(service, credential)
    destination = tmp_path / "exported-report.txt"

    code, output, errors = execute_cli(
        path, process_keys, credential, destination,
    )
    assert code == 0
    assert errors == ""
    assert destination.stat().st_size > 0
    assert "REPORTE DE REVISIÓN VM" in output
    assert "CASE" in output
    assert report.evaluations[0].criterion.statement in output
    assert report.evaluations[0].rationale in output
    assert "Atribución: DECLARADA" in output
    assert credential not in output


@pytest.mark.parametrize("failure", [
    "invalid_credential", "revoked", "absent", "configuration", "backend",
])
def test_process_error_codes_never_export_report_or_credential(
    tmp_path, process_keys, failure,
):
    path, service, grants, definitions = setup.environment(tmp_path, process_keys)
    credential = setup.token(process_keys[0])
    report = save_report(service, credential)
    report_id = "REPORT-1"
    include_key = True

    if failure == "invalid_credential":
        credential = setup.token(process_keys[1])
        expected_code = 3
    elif failure == "revoked":
        for index, grant in enumerate(definitions):
            assert grants.apply(record=GrantAdministrationRecord(
                f"PROCESS-REVOKE-{index}", grant.principal,
                Action.REVOKE, grant, int(setup.time.time()),
            ))
        expected_code = 4
    elif failure == "absent":
        report_id = "MISSING"
        expected_code = 5
    elif failure == "configuration":
        include_key = False
        expected_code = 2
    else:
        # Existing file, but not a SQLite database: infrastructure failure.
        path = tmp_path / "invalid-database.sqlite3"
        path.write_bytes(b"not a SQLite database")
        expected_code = 6

    destination = tmp_path / f"{failure}.txt"
    code, output, errors = execute_cli(
        path, process_keys, credential, destination,
        report_id=report_id, include_key=include_key,
    )
    assert code == expected_code, errors
    assert output == ""
    assert destination.stat().st_size == 0
    assert errors.strip()
    assert credential not in errors
    assert report.evaluations[0].rationale not in errors
    assert report.evaluations[0].criterion.statement not in errors
    assert "Traceback" not in errors
