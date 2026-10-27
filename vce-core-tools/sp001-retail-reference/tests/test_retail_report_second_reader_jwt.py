import time

import pytest

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture

from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)
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
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)
from sp001.services.authenticated_retail_reports import RetailReportAccessDenied


def test_signed_second_reader_preserves_admission_and_obeys_revocation(
    tmp_path, keys,
):
    path, service, grants, _ = setup.environment(tmp_path, keys)
    now = int(time.time())

    author = AuthenticatedPrincipal(setup.ISSUER, "SUBJECT")
    reviewer = AuthenticatedPrincipal(setup.ISSUER, "REVIEWER")
    report = setup.make_report()
    actor = report.evaluations[0].evaluator

    bindings = SqliteRetailEvaluatorBindings(database_path=path)
    binding = RetailEvaluatorBinding(
        "TEST-BINDING", 1, author, actor, "CASE", now - 10, now + 300,
    )
    bindings.apply(change=RetailEvaluatorBindingChange(
        "TEST-BINDING-EVENT",
        RetailEvaluatorBindingSnapshot(binding, False),
        author,
        now,
    ))

    service.save_with_admissions(
        credential=setup.token(keys[0]),
        identity=setup.IDENTITY,
        report=report,
        binding_references=(
            RetailEvaluationBindingReference("EVAL", "TEST-BINDING", 1),
        ),
    )

    read_permission = CaseAccessPermission(
        "CASE", CaseAccessOperation.READ_RETAIL_REPORT,
    )
    reviewer_grant = CaseAccessGrant(
        "REVIEWER-READ",
        reviewer,
        read_permission,
        now - 10,
        now + 300,
    )
    grants.apply(record=GrantAdministrationRecord(
        "REVIEWER-GRANT-EVENT",
        author,
        GrantAdministrationAction.GRANT,
        reviewer_grant,
        now,
    ))

    read_operations = (CaseAccessOperation.READ_RETAIL_REPORT,)
    reviewer_token = setup.token(
        keys[0],
        operations=read_operations,
        overrides={"sub": "REVIEWER"},
    )
    outsider_token = setup.token(
        keys[0],
        operations=read_operations,
        overrides={"sub": "OUTSIDER"},
    )

    recovered = service.recover_with_admissions(
        credential=reviewer_token,
        identity=setup.IDENTITY,
        case_id="CASE",
    )

    assert reviewer != author
    assert recovered is not None
    assert recovered.report == report
    assert recovered.declared_only_evaluation_ids == ()
    assert len(recovered.admissions) == 1
    assert recovered.admissions[0].principal == author
    assert recovered.admissions[0].evaluation == report.evaluations[0]

    # Un JWT firmado con el claim de lectura no sustituye la concesión local.
    with pytest.raises(RetailReportAccessDenied):
        service.recover_with_admissions(
            credential=outsider_token,
            identity=setup.IDENTITY,
            case_id="CASE",
        )

    grants.apply(record=GrantAdministrationRecord(
        "REVIEWER-REVOKE-EVENT",
        author,
        GrantAdministrationAction.REVOKE,
        reviewer_grant,
        int(time.time()),
    ))

    # La misma credencial deja de autorizar nuevas lecturas.
    with pytest.raises(RetailReportAccessDenied):
        service.recover_with_admissions(
            credential=reviewer_token,
            identity=setup.IDENTITY,
            case_id="CASE",
        )

    assert setup.row_count(path) == 1
