import json
import os
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, ProxyHandler, build_opener

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_authenticated_observation_operations_jwt import environment, request
from test_inspection_observation_host_bootstrap import configuration
from test_inspection_observation_bootstrap_operations import (
    operation_configuration,
)
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def test_uvicorn_operation_save_retry_recovery_and_revocation(tmp_path, keys):
    service, grants, definitions = environment(tmp_path, keys)
    database = Path(service._backend._path).resolve()
    config = operation_configuration(configuration(database, keys))
    child_env = os.environ.copy()
    # Prevent inherited observation configuration from affecting this test.
    prefix = "SP001_INSPECTION_OBSERVATION_"
    for name in list(child_env):
        if name.startswith(prefix):
            del child_env[name]
    child_env.update(config)
    child_env["PYTHONPATH"] = str(Path("src").resolve())

    item = request()
    document = serialize(item.observation)
    route_path = (
        f"/v1/cases/{item.observation.case_id}/"
        f"inspection-observation-operations/{item.request_id}"
    )
    opener = build_opener(ProxyHandler({}))
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    port = listener.getsockname()[1]
    url = f"http://127.0.0.1:{port}{route_path}"

    def call(method, credential=None, body=None, target=None):
        headers = {}
        if credential is not None:
            headers["Authorization"] = "Bearer " + credential
        data = None
        if body is not None:
            data = body.encode("utf-8")
            headers["Content-Type"] = "application/json"
        outgoing = Request(
            target or url, data=data, headers=headers, method=method,
        )
        try:
            response = opener.open(outgoing, timeout=1)
        except HTTPError as error:
            response = error
        with response:
            return (
                response.status,
                {key.lower(): value for key, value in response.headers.items()},
                json.loads(response.read().decode("utf-8")),
            )

    process = None
    log_path = tmp_path / "operation-uvicorn.log"
    try:
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                [
                    sys.executable, "-m", "uvicorn",
                    "sp001.infrastructure.inspection_observation_host_bootstrap:create_app",
                    "--factory", "--fd", str(listener.fileno()),
                    "--log-level", "warning", "--no-access-log",
                ],
                env=child_env,
                pass_fds=(listener.fileno(),),
                stdout=log, stderr=log,
            )

        deadline = time.monotonic() + 15
        while True:
            if process.poll() is not None:
                raise AssertionError(
                    f"host exited before readiness: {process.returncode}"
                )
            try:
                status, _, body = call("GET")
                assert status == 401
                assert body["status"] == "credential_rejected"
                break
            except (URLError, TimeoutError, OSError):
                if time.monotonic() >= deadline:
                    raise AssertionError("host readiness timeout")
                time.sleep(0.05)
        listener.close()

        # Generate credentials after host readiness, preserving normal TTL.
        credential = jwt_setup.token(
            keys[0], operations=(setup.SAVE, setup.READ),
        )
        invalid = jwt_setup.token(
            keys[1], operations=(setup.SAVE, setup.READ),
        )

        status, _, body = call("PUT", invalid, document)
        assert status == 401
        assert body["status"] == "credential_rejected"
        assert "observation_document" not in body

        status, _, body = call("GET", credential)
        assert status == 404
        assert body == {"status": "operation_not_found"}

        status, headers, saved = call("PUT", credential, document)
        assert status == 200
        assert saved["status"] == "saved"
        assert saved["disposition"] == "CREATED"
        assert "observation_document" not in saved
        assert headers["cache-control"] == "no-store"

        status, _, retry = call("PUT", credential, document)
        assert status == 200
        assert retry == saved

        status, headers, recovered = call("GET", credential)
        assert status == 200
        assert recovered["status"] == "ok"
        assert recovered["observation_document"] == document
        assert recovered["disposition"] == "CREATED"
        assert headers["cache-control"] == "no-store"

        for index, grant in enumerate(definitions):
            assert grants.apply(record=GrantAdministrationRecord(
                f"PROCESS-OP-REVOKE-{index}",
                grant.principal, Action.REVOKE, grant, int(time.time()),
            ))

        status, _, body = call("PUT", credential, document)
        assert status == 403
        assert body["status"] == "access_denied"
        assert "observation_document" not in body

        status, _, body = call("GET", credential)
        assert status == 403
        assert body["status"] == "access_denied"
        assert "observation_document" not in body

        with sqlite3.connect(database) as connection:
            for table in (
                "retail_inspection_observations",
                "retail_observation_operations",
            ):
                assert connection.execute(
                    "SELECT COUNT(*) FROM " + table
                ).fetchone()[0] == 1
    finally:
        listener.close()
        if process is not None:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            else:
                process.wait(timeout=5)
