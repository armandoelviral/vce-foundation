import http.client
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import time

import pytest

from test_case_state_https_loopback import certificates
import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_retail_report_host_bootstrap import configuration

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)


def test_https_process_checks_trust_hostname_and_revocation(tmp_path, keys):
    database, service, grants, definitions = setup.environment(tmp_path, keys)
    credential = setup.token(keys[0])

    service.save(
        credential=credential,
        identity=setup.IDENTITY,
        report=setup.make_report(),
    )

    tls_directory = tmp_path / "server-tls"
    tls_directory.mkdir()
    ca, certificate, tls_key = certificates(tls_directory)

    other_directory = tmp_path / "unrelated-ca"
    other_directory.mkdir()
    other_ca, _, _ = certificates(other_directory)

    trusted_context = ssl.create_default_context(cafile=str(ca))
    unrelated_context = ssl.create_default_context(cafile=str(other_ca))

    environment = os.environ.copy()
    environment.update(configuration(database, keys))
    environment["PYTHONPATH"] = str(Path("src").resolve())

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    port = listener.getsockname()[1]

    target = "/v1/cases/CASE/retail-reports/REPORT-1"

    def request(context, hostname="localhost", token=None):
        connection = http.client.HTTPSConnection(
            hostname, port, context=context, timeout=1,
        )
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        try:
            connection.request("GET", target, headers=headers)
            response = connection.getresponse()
            return (
                response.status,
                {name.lower(): value for name, value in response.getheaders()},
                json.loads(response.read().decode("utf-8")),
            )
        finally:
            connection.close()

    process = None

    try:
        with (tmp_path / "uvicorn-https.log").open("wb") as log:
            process = subprocess.Popen(
                [
                    sys.executable, "-m", "uvicorn",
                    "sp001.infrastructure.retail_report_host_bootstrap:create_app",
                    "--factory",
                    "--fd", str(listener.fileno()),
                    "--ssl-certfile", str(certificate),
                    "--ssl-keyfile", str(tls_key),
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
                status, _, body = request(trusted_context)
                assert status == 401
                assert body == {"status": "credential_rejected"}
                break
            except ssl.SSLCertVerificationError:
                # Un fallo de confianza no se trata como espera de arranque.
                raise
            except (OSError, TimeoutError):
                if time.monotonic() >= deadline:
                    raise AssertionError("HTTPS no respondió a tiempo")
                time.sleep(0.05)

        listener.close()

        # CA confiable y nombre correcto.
        status, headers, body = request(
            trusted_context, token=credential,
        )
        assert status == 200
        assert body["status"] == "ok"
        assert body["report_text"]
        assert headers["cache-control"] == "no-store"

        # El cliente confía en otra CA: debe rechazar al servidor.
        with pytest.raises(ssl.SSLCertVerificationError):
            request(unrelated_context, token=credential)

        # La cadena es confiable, pero el certificado no incluye la IP.
        with pytest.raises(ssl.SSLCertVerificationError):
            request(
                trusted_context,
                hostname="127.0.0.1",
                token=credential,
            )

        # Revocación local confirmada mientras el servidor sigue activo.
        for index, grant in enumerate(definitions):
            assert grants.apply(record=GrantAdministrationRecord(
                f"HTTPS-REVOKE-{index}",
                grant.principal,
                GrantAdministrationAction.REVOKE,
                grant,
                int(time.time()),
            ))

        # TLS sigue siendo válido; la autorización de negocio es denegada.
        status, headers, body = request(
            trusted_context, token=credential,
        )
        assert status == 403
        assert body == {"status": "access_denied"}
        assert headers["cache-control"] == "no-store"
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
