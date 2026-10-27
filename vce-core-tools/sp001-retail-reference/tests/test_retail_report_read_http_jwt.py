import time

import pytest
from fastapi.testclient import TestClient

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

from sp001.contracts.case_access_context import CaseAccessOperation
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)
from sp001.infrastructure.retail_report_read_http_host import (
    create_retail_report_read_app,
)


ROUTE = "/v1/cases/CASE/retail-reports/REPORT-1"


def test_http_host_uses_signed_jwt_and_current_sqlite_grants(tmp_path, keys):
    path, service, grants, definitions = setup.environment(tmp_path, keys)

    author_token = setup.token(keys[0])
    report = setup.make_report()

    # El fixture guarda un reporte con atribución declarada.
    service.save(
        credential=author_token,
        identity=setup.IDENTITY,
        report=report,
    )

    client = TestClient(create_retail_report_read_app(service=service))

    read_token = setup.token(
        keys[0],
        operations=(CaseAccessOperation.READ_RETAIL_REPORT,),
    )
    accepted = client.get(
        ROUTE,
        headers={"Authorization": f"Bearer {read_token}"},
    )

    assert accepted.status_code == 200
    assert accepted.json()["status"] == "ok"
    assert accepted.json()["report_text"]
    assert accepted.headers["cache-control"] == "no-store"

    # Firma inválida: debe rechazarse antes de devolver contenido.
    wrong_signature = setup.token(keys[1])
    rejected = client.get(
        ROUTE,
        headers={"Authorization": f"Bearer {wrong_signature}"},
    )
    assert rejected.status_code == 401
    assert rejected.json() == {"status": "credential_rejected"}

    # Token válido y claim de lectura, pero sin concesión local.
    outsider = setup.token(
        keys[0],
        operations=(CaseAccessOperation.READ_RETAIL_REPORT,),
        overrides={"sub": "OUTSIDER"},
    )
    denied = client.get(
        ROUTE,
        headers={"Authorization": f"Bearer {outsider}"},
    )
    assert denied.status_code == 403
    assert denied.json() == {"status": "access_denied"}

    # Ausencia solo después de una consulta autorizada.
    missing = client.get(
        "/v1/cases/CASE/retail-reports/MISSING",
        headers={"Authorization": f"Bearer {read_token}"},
    )
    assert missing.status_code == 404
    assert missing.json() == {"status": "report_not_found"}

    # Revocación local: el mismo JWT deja de permitir la lectura.
    for index, grant in enumerate(definitions):
        grants.apply(record=GrantAdministrationRecord(
            f"HTTP-JWT-REVOKE-{index}",
            grant.principal,
            GrantAdministrationAction.REVOKE,
            grant,
            int(time.time()),
        ))

    revoked = client.get(
        ROUTE,
        headers={"Authorization": f"Bearer {read_token}"},
    )
    assert revoked.status_code == 403
    assert revoked.json() == {"status": "access_denied"}

    # Las lecturas y denegaciones no agregan reportes.
    assert setup.row_count(path) == 1
