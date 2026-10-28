import sqlite3
import time

from fastapi.testclient import TestClient

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

from sp001.contracts.case_access_context import CaseAccessOperation
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluation_binding_reference import (
    RetailEvaluationBindingReference,
)
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding,
    RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)
from sp001.infrastructure.retail_report_read_http_host import (
    create_retail_report_read_app,
)
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)
from sp001.services.retail_vm_report_text import render_retail_vm_report_text


def test_http_returns_report_with_recorded_admission(tmp_path, keys):
    path, service, _, _ = setup.environment(tmp_path, keys)
    now = int(time.time())

    author = AuthenticatedPrincipal(setup.ISSUER, "SUBJECT")
    report = setup.make_report()

    binding = RetailEvaluatorBinding(
        "HTTP-BINDING",
        1,
        author,
        report.evaluations[0].evaluator,
        "CASE",
        now - 10,
        now + 300,
    )

    bindings = SqliteRetailEvaluatorBindings(database_path=path)
    bindings.apply(change=RetailEvaluatorBindingChange(
        "HTTP-BINDING-EVENT",
        RetailEvaluatorBindingSnapshot(binding, False),
        author,
        now,
    ))

    service.save_with_admissions(
        credential=setup.token(keys[0]),
        identity=setup.IDENTITY,
        report=report,
        binding_references=(
            RetailEvaluationBindingReference(
                "EVAL", "HTTP-BINDING", 1,
            ),
        ),
    )

    read_token = setup.token(
        keys[0],
        operations=(CaseAccessOperation.READ_RETAIL_REPORT,),
    )

    # Comprobar la admisión recuperada por la fachada.
    recovered = service.recover_with_admissions(
        credential=read_token,
        identity=setup.IDENTITY,
        case_id="CASE",
    )

    assert recovered is not None
    assert recovered.report == report
    assert recovered.declared_only_evaluation_ids == ()
    assert len(recovered.admissions) == 1

    admission = recovered.admissions[0]
    assert admission.principal == author
    assert admission.evaluation == report.evaluations[0]
    assert admission.binding_snapshot.binding.binding_id == "HTTP-BINDING"
    assert admission.binding_snapshot.binding.revision == 1

    expected_text = render_retail_vm_report_text(
        identity=setup.IDENTITY,
        recovered=recovered,
    )

    client = TestClient(create_retail_report_read_app(service=service))
    response = client.get(
        "/v1/cases/CASE/retail-reports/REPORT-1",
        headers={"Authorization": f"Bearer {read_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "report_text": expected_text,
    }
    assert response.headers["cache-control"] == "no-store"

    # La lectura HTTP no duplica reporte ni admisión.
    with sqlite3.connect(path) as connection:
        report_count = connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0]
        admission_count = connection.execute(
            "SELECT COUNT(*) FROM retail_evaluation_admissions"
        ).fetchone()[0]

    assert report_count == 1
    assert admission_count == 1
