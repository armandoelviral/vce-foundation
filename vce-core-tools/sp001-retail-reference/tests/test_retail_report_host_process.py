import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, ProxyHandler, build_opener

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)


def test_uvicorn_process_enforces_report_access_over_loopback(tmp_path, keys):
    database, service, grants, definitions = setup.environment(tmp_path, keys)
    report = setup.make_report()
    credential = setup.token(keys[0])

    service.save(
        credential=credential,
        identity=setup.IDENTITY,
        report=report,
    )

    environment = os.environ.copy()
    environment.update({
        "PYTHONPATH": str(Path("src").resolve()),
        "SP001_RETAIL_REPORT_DATABASE": str(database.resolve()),
        "SP001_RETAIL_REPORT_ISSUER": setup.ISSUER,
        "SP001_RETAIL_REPORT_AUDIENCE": setup.AUDIENCE,
        "SP001_RETAIL_REPORT_KEY_ID": "KEY-1",
        "SP001_RETAIL_REPORT_PUBLIC_KEY_PEM":
            keys[0].public_key().public_bytes(
                Encoding.PEM,
                PublicFormat.SubjectPublicKeyInfo,
            ).decode("ascii"),
        "SP001_RETAIL_REPORT_MAX_LIFETIME_SECONDS": "120",
        "SP001_RETAIL_REPORT_MAX_TOKEN_BYTES": "16384",
    })

    # Puerto reservado y descriptor heredado: evita liberar el puerto
    # entre su selección y el arranque del servidor.
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    port = listener.getsockname()[1]

    opener = build_opener(ProxyHandler({}))
    route = f"http://127.0.0.1:{port}/v1/cases/CASE/retail-reports/REPORT-1"

    def request(url, token=None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

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
    log_path = tmp_path / "uvicorn.log"

    try:
        with log_path.open("wb") as log:
            process = subprocess.Popen(
                [
                    sys.executable, "-m", "uvicorn",
                    "sp001.infrastructure.retail_report_host_bootstrap:create_app",
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
                    f"Uvicorn terminó antes de iniciar: {process.returncode}"
                )

            try:
                status, _, body = request(route)
                assert status == 401
                assert body == {"status": "credential_rejected"}
                break
            except (URLError, TimeoutError, OSError):
                if time.monotonic() >= deadline:
                    raise AssertionError("Uvicorn no respondió a tiempo")
                time.sleep(0.05)

        # La apertura del socket ya pertenece al proceso servidor.
        listener.close()

        status, headers, body = request(route, credential)
        assert status == 200
        assert body["status"] == "ok"
        assert body["report_text"]
        assert headers.get("cache-control") == "no-store"

        status, _, body = request(route, "invalid-credential")
        assert status == 401
        assert body == {"status": "credential_rejected"}

        missing_route = (
            f"http://127.0.0.1:{port}"
            "/v1/cases/CASE/retail-reports/MISSING"
        )
        status, _, body = request(missing_route, credential)
        assert status == 404
        assert body == {"status": "report_not_found"}

        # Revocación confirmada en SQLite por el proceso de prueba.
        for index, grant in enumerate(definitions):
            assert grants.apply(record=GrantAdministrationRecord(
                f"PROCESS-REVOKE-{index}",
                grant.principal,
                GrantAdministrationAction.REVOKE,
                grant,
                int(time.time()),
            ))

        # El mismo JWT ya no permite la lectura en el otro proceso.
        status, _, body = request(route, credential)
        assert status == 403
        assert body == {"status": "access_denied"}

        assert setup.row_count(database) == 1

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
