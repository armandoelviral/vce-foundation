import sqlite3
from dataclasses import replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation, CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import RetailRuleEvaluationRecord
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_authorized_retail_report_writer import (
    SqliteAuthorizedRetailReportWriter,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)
from sp001.services.transactional_authenticated_retail_reports import (
    TransactionalAuthenticatedRetailReports,
)


def make_report():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    record = RetailRuleEvaluationRecord(
        "EVAL",
        RetailContextRuleObservation(
            "OBS", "RULE", "SNAPSHOT", 1, "CASE",
            RuleObservationStatus.CONFORMANT, ("EVIDENCE",),
        ),
        RetailRuleCriterion("RULE", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic rationale.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE", evaluations=(record,),
    )


class Authenticator:
    def __init__(self, access):
        self.access = access
        self.calls = 0

    def authenticate(self, *, credential):
        self.calls += 1
        return self.access if credential == "valid" else None


def environment(tmp_path):
    path = tmp_path / "shared.sqlite3"
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    permissions = tuple(
        CaseAccessPermission("CASE", operation)
        for operation in (
            Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
        )
    )
    access = ValidatedCaseAccessContext(
        principal, "REPORTS", 100, 100, 200, permissions,
    )
    grants = SqliteCaseAccessGrants(database_path=path)
    definitions = []
    for index, permission in enumerate(permissions):
        grant = CaseAccessGrant(
            f"GRANT-{index}", principal, permission, 100, 300,
        )
        assert grants.apply(record=GrantAdministrationRecord(
            f"EVENT-{index}", principal, Action.GRANT, grant, 100,
        ))
        definitions.append(grant)
    auth = Authenticator(access)
    backend = SqliteAuthorizedRetailReportWriter(
        database_path=path, expected_audience="REPORTS", clock=lambda: 150,
    )
    service = TransactionalAuthenticatedRetailReports(
        authenticator=auth, backend=backend,
        expected_audience="REPORTS", clock=lambda: 150,
    )
    return path, grants, definitions, auth, backend, service


IDENTITY = RetailRuleEvaluationReportIdentity("REPORT")


def test_facade_saves_retries_and_recovers_through_real_backend(tmp_path):
    path, _, _, auth, _, service = environment(tmp_path)
    report = make_report()
    assert service.save(
        credential="valid", identity=IDENTITY, report=report
    ) == report
    assert service.save(
        credential="valid", identity=IDENTITY, report=report
    ) == report
    assert service.recover(
        credential="valid", identity=IDENTITY, case_id="CASE"
    ) == report
    assert auth.calls == 3
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0] == 1


def test_revoked_grants_block_retries_and_recovery(tmp_path):
    _, grants, definitions, auth, _, service = environment(tmp_path)
    report = make_report()
    service.save(credential="valid", identity=IDENTITY, report=report)
    for index, grant in enumerate(definitions):
        assert grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{index}", auth.access.principal,
            Action.REVOKE, grant, 150,
        ))
    with pytest.raises(RetailReportAccessDenied):
        service.save(credential="valid", identity=IDENTITY, report=report)
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE"
        )
    assert auth.calls == 3


def test_invalid_credential_and_insufficient_claims_never_call_backend(tmp_path):
    _, _, _, auth, backend, service = environment(tmp_path)
    calls = []

    def unexpected(**kwargs):
        calls.append(kwargs)
        raise AssertionError("backend must not be called")

    backend.save_authorized = unexpected
    with pytest.raises(RetailReportAuthenticationRejected):
        service.save(
            credential="invalid", identity=IDENTITY, report=make_report()
        )
    auth.access = replace(auth.access, permissions=())
    with pytest.raises(RetailReportAccessDenied):
        service.save(
            credential="valid", identity=IDENTITY, report=make_report()
        )
    assert calls == []


def test_authenticator_failure_is_not_credential_rejection(tmp_path):
    _, _, _, auth, _, service = environment(tmp_path)
    failure = OSError("synthetic authentication provider failure")

    def broken(**kwargs):
        raise failure

    auth.authenticate = broken
    with pytest.raises(OSError) as caught:
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE"
        )
    assert caught.value is failure


def test_backend_receives_exact_authenticated_context_and_expected_case(tmp_path):
    _, _, _, auth, backend, service = environment(tmp_path)
    calls = []

    def recover(**kwargs):
        calls.append(kwargs)
        return None

    backend.recover_authorized = recover
    assert service.recover(
        credential="valid", identity=IDENTITY, case_id="CASE"
    ) is None
    assert calls[0]["access"] is auth.access
    assert calls[0]["identity"] is IDENTITY
    assert calls[0]["case_id"] == "CASE"


def test_checks_validity_again_after_backend_returns(tmp_path):
    _, _, _, auth, backend, _ = environment(tmp_path)
    now = [150]
    service = TransactionalAuthenticatedRetailReports(
        authenticator=auth, backend=backend,
        expected_audience="REPORTS", clock=lambda: now[0],
    )

    def recover(**kwargs):
        now[0] = 200
        return make_report()

    backend.recover_authorized = recover
    with pytest.raises(RetailReportAuthenticationRejected):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE"
        )


def test_facade_rejects_wrong_case_returned_by_backend(tmp_path):
    _, _, _, auth, backend, service = environment(tmp_path)
    auth.access = replace(
        auth.access,
        permissions=(CaseAccessPermission(
            "OTHER", Operation.READ_RETAIL_REPORT,
        ),),
    )
    backend.recover_authorized = lambda **kwargs: make_report()
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="OTHER"
        )


def test_rejects_backend_without_authorized_operations(tmp_path):
    _, _, _, auth, _, _ = environment(tmp_path)

    class UnprotectedBackend:
        def save(self, **kwargs):
            return None

        def recover(self, **kwargs):
            return None

    with pytest.raises(TypeError, match="authorized operations"):
        TransactionalAuthenticatedRetailReports(
            authenticator=auth, backend=UnprotectedBackend(),
            expected_audience="REPORTS", clock=lambda: 150,
        )
