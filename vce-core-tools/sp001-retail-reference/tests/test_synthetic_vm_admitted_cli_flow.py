import sqlite3
import time
from dataclasses import replace

from cryptography.hazmat.primitives.asymmetric import rsa

import test_retail_report_jwt_composition as setup
import test_retail_vm_report_cli_process as process

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)
from sp001.contracts.retail_evaluation_binding_reference import (
    RetailEvaluationBindingReference,
)
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)


def stored_documents(path):
    with sqlite3.connect(path) as connection:
        return (
            connection.execute(
                "SELECT report_id, document FROM retail_rule_evaluation_reports"
            ).fetchall(),
            connection.execute(
                "SELECT evaluation_id, document FROM retail_evaluation_admissions"
            ).fetchall(),
        )


def test_synthetic_vm_admission_and_cli_export(tmp_path):
    # Synthetic credentials, authority provisioning and evaluation: test only.
    keys = tuple(
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        for _ in range(2)
    )
    path, service, _, _ = setup.environment(tmp_path, keys)
    report = setup.make_report()
    evaluation = replace(
        report.evaluations[0],
        criterion=replace(
            report.evaluations[0].criterion,
            statement="CASO SINTÉTICO: comprobar la posición declarada del mueble.",
        ),
        rationale=(
            "Resultado sintético suministrado por el test. "
            "No se inspeccionaron imágenes ni se verificaron medidas físicas."
        ),
    )
    report = replace(report, evaluations=(evaluation,))
    principal = AuthenticatedPrincipal(setup.ISSUER, "SUBJECT")
    now = int(time.time())
    binding = RetailEvaluatorBinding(
        "VM-SYNTHETIC-BINDING", 1, principal, evaluation.evaluator,
        report.case_id, now - 10, now + 600,
    )
    bindings = SqliteRetailEvaluatorBindings(database_path=path)
    assert bindings.apply(change=RetailEvaluatorBindingChange(
        "VM-SYNTHETIC-BINDING-CREATED",
        RetailEvaluatorBindingSnapshot(binding, False), principal, now,
    ))

    credential = setup.token(keys[0])
    assert service.save_with_admissions(
        credential=credential, identity=setup.IDENTITY, report=report,
        binding_references=(RetailEvaluationBindingReference(
            evaluation.evaluation_id, binding.binding_id, 1,
        ),),
    ) == report

    recovered = service.recover_with_admissions(
        credential=credential, identity=setup.IDENTITY, case_id=report.case_id,
    )
    assert recovered.report == report
    assert recovered.declared_only_evaluation_ids == ()
    assert len(recovered.admissions) == 1
    admission = recovered.admissions[0]
    assert admission.evaluation == evaluation
    assert admission.principal == principal
    assert admission.binding_snapshot.binding == binding

    before_export = stored_documents(path)
    assert tuple(map(len, before_export)) == (1, 1)
    destination = tmp_path / "synthetic-vm-report.txt"
    code, output, errors = process.execute_cli(
        path, keys, credential, destination,
    )
    assert code == 0, errors
    assert errors == ""
    assert "CASO SINTÉTICO" in output
    assert evaluation.rationale in output
    assert "ADMISIÓN LOCAL REGISTRADA" in output
    assert binding.binding_id in output
    assert "Revisión utilizada: 1" in output
    assert principal.subject in output
    assert "no equivale a aprobación" in output
    assert credential not in output
    assert destination.stat().st_size > 0
    assert stored_documents(path) == before_export
