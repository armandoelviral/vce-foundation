import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction,
    GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.services.authenticated_retail_reports import RetailReportAccessDenied
from sp001.services.transactional_authenticated_retail_reports import (
    TransactionalAuthenticatedRetailReports,
)


def test_second_authorized_principal_recovers_original_admission(tmp_path):
    (
        path, now, author, report, _, _, grants, _,
        _, backend, author_service,
    ) = setup.environment(tmp_path)

    # El autor guarda el reporte y su admisión original.
    setup.save(author_service, report)

    reviewer = AuthenticatedPrincipal("ISSUER", "REVIEWER")
    outsider = AuthenticatedPrincipal("ISSUER", "OUTSIDER")

    permission = CaseAccessPermission(
        "CASE", CaseAccessOperation.READ_RETAIL_REPORT,
    )

    grant = CaseAccessGrant(
        "REVIEWER-READ-GRANT", reviewer, permission, 100, 300,
    )
    grants.apply(record=GrantAdministrationRecord(
        "REVIEWER-READ-EVENT",
        author,
        GrantAdministrationAction.GRANT,
        grant,
        100,
    ))

    class Authenticator:
        def authenticate(self, *, credential):
            principal = {
                "reviewer-token": reviewer,
                "outsider-token": outsider,
            }.get(credential)

            if principal is None:
                return None

            # Ambos contextos declaran lectura. Solo reviewer tiene
            # además una concesión local vigente.
            return ValidatedCaseAccessContext(
                principal,
                "REPORTS",
                100,
                100,
                300,
                (permission,),
            )

    service = TransactionalAuthenticatedRetailReports(
        authenticator=Authenticator(),
        backend=backend,
        expected_audience="REPORTS",
        clock=lambda: now[0],
    )

    recovered = service.recover_with_admissions(
        credential="reviewer-token",
        identity=setup.Identity("REPORT"),
        case_id="CASE",
    )

    assert reviewer != author
    assert recovered is not None
    assert recovered.report == report
    assert recovered.declared_only_evaluation_ids == ()
    assert len(recovered.admissions) == 1

    # La lectura por otra persona conserva la atribución original.
    admission = recovered.admissions[0]
    assert admission.principal == author
    assert admission.evaluation == report.evaluations[0]
    assert admission.binding_snapshot.binding.revision == 1

    before = setup.counts(path)

    with pytest.raises(RetailReportAccessDenied):
        service.recover_with_admissions(
            credential="outsider-token",
            identity=setup.Identity("REPORT"),
            case_id="CASE",
        )

    # Ni la lectura autorizada ni la denegada crean registros nuevos.
    assert setup.counts(path) == before == (1, 1)
