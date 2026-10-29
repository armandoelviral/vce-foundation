import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, ProxyHandler, build_opener

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
from test_inspection_observation_host_bootstrap import configuration

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def test_uvicorn_process_enforces_observation_access(tmp_path, keys):
    database, service, _, grants, definitions = setup.environment(tmp_path, keys)
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))
    expected = serialize(item)

    environment = os.environ.copy()
    environment.update(configuration(database.resolve(), keys))
    environment["PYTHONPATH"] = str(Path("src").resolve())

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    port = listener.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    route = (
        base + "/v1/cases/CASE/inspection-observations/OBS-1/versions/1"
    )
    missing = (
        base + "/v1/cases/CASE/inspection-observations/MISSING/versions/1"
    )
    opener = build_opener(ProxyHandler({}))

    def request(url, token=None):
        headers = {} if token is None else {
            "Authorization": f"Bearer {token}",
        }
        req = Request(url, headers=headers, method="GET")
        try:
            response = opener.open(req, timeout=1)
        except HTTPError as error:
            response = error
        with response:
            return (
                response.status,
                {name.lower(): value for name, value in response.headers.items()},
                json.loads(response.read().decode("utf-8")),
            )

    process = None
    log_path = tmp_path / "uvicorn-observations.log"
    try:
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                [
                    sys.executable, "-m", "uvicorn",
                    "sp001.infrastructure.inspection_observation_host_bootstrap:create_app",
                    "--factory",
                    "--fd", str(listener.fileno()),
                    "--log-level", "warning",
                    "--no-access-log",
                ],
                env=environment,
                pass_fds=(listener.fileno(),),
                stdout=log,
                stderr=log,
            )

        deadline = time.monotonic() + 15
        while True:
            if process.poll() is not None:
                raise AssertionError(
                    f"Uvicorn exited before readiness: {process.returncode}"
                )
            try:
                status, _, body = request(route)
                assert status == 401
                assert body == {"status": "credential_rejected"}
                break
            except (URLError, TimeoutError, OSError):
                if time.monotonic() >= deadline:
                    raise AssertionError("Uvicorn readiness timeout")
                time.sleep(0.05)

        listener.close()

        status, headers, body = request(route, credential)
        assert status == 200
        assert headers["cache-control"] == "no-store"
        assert body == {"status": "ok", "observation_document": expected}

        status, headers, body = request(route, "invalid-credential")
        assert status == 401
        assert headers["cache-control"] == "no-store"
        assert body == {"status": "credential_rejected"}

        save_only = jwt_setup.token(keys[0], operations=(setup.SAVE,))
        status, _, body = request(route, save_only)
        assert status == 403
        assert body == {"status": "access_denied"}

        status, _, body = request(missing, credential)
        assert status == 404
        assert body == {"status": "observation_not_found"}

        read_grant = next(
            definition for definition in definitions
            if definition.permission.operation is setup.READ
        )
        assert grants.apply(record=GrantAdministrationRecord(
            "PROCESS-REVOKE-OBSERVATION-READ",
            read_grant.principal, Action.REVOKE, read_grant,
            int(time.time()),
        ))

        # The child process must observe the committed local revocation.
        status, headers, body = request(route, credential)
        assert status == 403
        assert headers["cache-control"] == "no-store"
        assert body == {"status": "access_denied"}
        assert setup.count(database) == 1
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
                process.wait()

    # Access logging is disabled; no credential or observation body is expected.
    log = log_path.read_text(errors="replace")
    assert credential not in log
    assert expected not in log
