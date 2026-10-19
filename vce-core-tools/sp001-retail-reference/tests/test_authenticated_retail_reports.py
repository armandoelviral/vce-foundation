from datetime import datetime, timezone

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission as Permission,
    ValidatedCaseAccessContext,
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
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)
from sp001.services.authenticated_retail_reports import (
    AuthenticatedRetailReports,
    RetailReportAccessDenied,
    RetailReportAuthenticationRejected,
)


def make_report():
    actor = RetailProcessActor(
        "ACTOR-TEST", "CUSTOMER-TEST", ActorType.HUMAN, "ORG-TEST",
        RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "VM reviewer"),
    )
    record = RetailRuleEvaluationRecord(
        "EVAL-1",
        RetailContextRuleObservation(
            "OBS-1", "RULE-1", "SNAPSHOT-1", 1, "CASE-1",
            RuleObservationStatus.CONFORMANT, ("EVIDENCE-1",),
        ),
        RetailRuleCriterion("RULE-1", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic rationale.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE-1", evaluations=(record,),
    )


class Authenticator:
    def __init__(self, permissions):
        self.calls = 0
        self.context = ValidatedCaseAccessContext(
            AuthenticatedPrincipal("ISSUER-TEST", "SUBJECT-TEST"),
            "REPORTS-TEST", 100, 100, 200, permissions,
        )

    def authenticate(self, *, credential):
        self.calls += 1
        return self.context if credential == "valid" else None


class Grants:
    def __init__(self):
        self.allowed = True
        self.calls = []

    def permits(self, *, principal, permission, at_time):
        self.calls.append((principal, permission, at_time))
        return self.allowed


class Backend:
    def __init__(self):
        self.report = None
        self.save_calls = 0
        self.read_calls = 0
        self.after = lambda: None

    def save(self, *, identity, report):
        self.save_calls += 1
        self.report = report
        self.after()
        return report

    def recover(self, *, identity):
        self.read_calls += 1
        self.after()
        return self.report


def setup(*, case_id="CASE-1", operations=None):
    if operations is None:
        operations = (Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT)
    auth = Authenticator(tuple(Permission(case_id, op) for op in operations))
    grants = Grants()
    backend = Backend()
    now = [150]
    service = AuthenticatedRetailReports(
        authenticator=auth, grants=grants, persistence=backend,
        expected_audience="REPORTS-TEST", clock=lambda: now[0],
    )
    return service, auth, grants, backend, now


IDENTITY = RetailRuleEvaluationReportIdentity("REPORT-1")


def test_save_and_recovery_check_exact_principal_case_and_permissions():
    service, auth, grants, backend, _ = setup()
    report = make_report()
    assert service.save(
        credential="valid", identity=IDENTITY, report=report
    ) == report
    assert service.recover(
        credential="valid", identity=IDENTITY, case_id="CASE-1"
    ) == report
    assert auth.calls == 2
    assert len(grants.calls) == 6
    assert all(call[0] == auth.context.principal for call in grants.calls)
    assert all(call[1].case_id == "CASE-1" for call in grants.calls)


def test_rejected_credential_never_reaches_backend():
    service, _, grants, backend, _ = setup()
    with pytest.raises(RetailReportAuthenticationRejected):
        service.recover(
            credential="invalid", identity=IDENTITY, case_id="CASE-1"
        )
    assert grants.calls == []
    assert backend.read_calls == 0


@pytest.mark.parametrize("operations", [
    (), (Operation.READ_STATE,), (Operation.SAVE_RETAIL_REPORT,),
])
def test_save_requires_both_report_permissions(operations):
    service, _, _, backend, _ = setup(operations=operations)
    with pytest.raises(RetailReportAccessDenied):
        service.save(
            credential="valid", identity=IDENTITY, report=make_report()
        )
    assert backend.save_calls == 0


def test_local_revocation_blocks_save_retry_and_recovery():
    service, auth, grants, backend, _ = setup()
    report = make_report()
    service.save(credential="valid", identity=IDENTITY, report=report)
    grants.allowed = False
    with pytest.raises(RetailReportAccessDenied):
        service.save(credential="valid", identity=IDENTITY, report=report)
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-1"
        )
    assert auth.calls == 3
    assert backend.save_calls == 1
    assert backend.read_calls == 0


def test_known_identity_does_not_allow_cross_case_disclosure():
    service, _, _, backend, _ = setup(case_id="CASE-2")
    backend.report = make_report()
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-2"
        )


def test_revocation_during_read_prevents_return():
    service, _, grants, backend, _ = setup()
    backend.report = make_report()
    backend.after = lambda: setattr(grants, "allowed", False)
    with pytest.raises(RetailReportAccessDenied):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-1"
        )


def test_expiry_during_read_prevents_return():
    service, _, _, backend, now = setup()
    backend.report = make_report()
    backend.after = lambda: now.__setitem__(0, 200)
    with pytest.raises(RetailReportAuthenticationRejected):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-1"
        )


def test_post_save_revocation_denies_return_but_does_not_undo_write():
    service, _, grants, backend, _ = setup()
    report = make_report()
    backend.after = lambda: setattr(grants, "allowed", False)
    with pytest.raises(RetailReportAccessDenied):
        service.save(credential="valid", identity=IDENTITY, report=report)
    assert backend.report == report


def test_provider_failure_propagates_without_storage_access():
    service, _, grants, backend, _ = setup()
    failure = OSError("synthetic grant provider failure")

    def broken(**kwargs):
        raise failure

    grants.permits = broken
    with pytest.raises(OSError) as caught:
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-1"
        )
    assert caught.value is failure
    assert backend.read_calls == 0


def test_non_boolean_grant_result_is_provider_error():
    service, _, grants, backend, _ = setup()
    grants.allowed = 1
    with pytest.raises(TypeError, match="exact bool"):
        service.recover(
            credential="valid", identity=IDENTITY, case_id="CASE-1"
        )
    assert backend.read_calls == 0


def test_authorized_absence_is_none():
    service, _, _, _, _ = setup(operations=(Operation.READ_RETAIL_REPORT,))
    assert service.recover(
        credential="valid", identity=IDENTITY, case_id="CASE-1"
    ) is None
