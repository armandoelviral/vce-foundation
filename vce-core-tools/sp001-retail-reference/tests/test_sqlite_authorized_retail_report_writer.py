import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Event

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


def environment(tmp_path, clock=None, writer_type=SqliteAuthorizedRetailReportWriter):
    path = tmp_path / "shared.sqlite3"
    grants = SqliteCaseAccessGrants(database_path=path)
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    permissions = tuple(
        CaseAccessPermission("CASE", operation)
        for operation in (
            Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
        )
    )
    definitions = []
    for index, permission in enumerate(permissions):
        grant = CaseAccessGrant(
            f"GRANT-{index}", principal, permission, 100, 300,
        )
        assert grants.apply(record=GrantAdministrationRecord(
            f"EVENT-{index}", principal, Action.GRANT, grant, 100,
        ))
        definitions.append(grant)
    access = ValidatedCaseAccessContext(
        principal, "REPORTS", 100, 100, 200, permissions,
    )
    writer = writer_type(
        database_path=path, expected_audience="REPORTS",
        clock=clock or (lambda: 150),
    )
    return path, grants, definitions, access, writer


def count(path):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM retail_rule_evaluation_reports"
        ).fetchone()[0]


def test_retry_rechecks_real_revoked_grant(tmp_path):
    path, grants, definitions, access, writer = environment(tmp_path)
    report = make_report()
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    assert writer.save_authorized(
        access=access, identity=identity, report=report
    ) == report
    assert grants.apply(record=GrantAdministrationRecord(
        "REVOKE", access.principal, Action.REVOKE, definitions[0], 151,
    ))
    with pytest.raises(RetailReportAccessDenied):
        writer.save_authorized(
            access=access, identity=identity, report=report
        )
    assert count(path) == 1


def test_expiry_after_actual_lock_wait_prevents_insert(tmp_path):
    attempted = Event()
    now = [150]

    class SignalledConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            if sql == "BEGIN IMMEDIATE":
                attempted.set()
            return super().execute(sql, parameters)

    class Writer(SqliteAuthorizedRetailReportWriter):
        def _connect(self):
            connection = sqlite3.connect(
                self._path, timeout=5, isolation_level=None,
                factory=SignalledConnection,
            )
            connection.execute("PRAGMA synchronous=FULL")
            return connection

    path, _, _, access, writer = environment(
        tmp_path, clock=lambda: now[0], writer_type=Writer,
    )
    blocker = sqlite3.connect(path, isolation_level=None)
    blocker.execute("BEGIN IMMEDIATE")
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                writer.save_authorized,
                access=access,
                identity=RetailRuleEvaluationReportIdentity("REPORT"),
                report=make_report(),
            )
            try:
                assert attempted.wait(timeout=3)
                assert not future.done()
                now[0] = 200
            finally:
                blocker.execute("ROLLBACK")
            with pytest.raises(RetailReportAuthenticationRejected):
                future.result(timeout=5)
    finally:
        if blocker.in_transaction:
            blocker.rollback()
        blocker.close()
    assert count(path) == 0


def test_expiry_before_commit_rolls_back_insert(tmp_path):
    instants = iter((150, 200))
    path, _, _, access, writer = environment(
        tmp_path, clock=lambda: next(instants),
    )
    with pytest.raises(RetailReportAuthenticationRejected):
        writer.save_authorized(
            access=access,
            identity=RetailRuleEvaluationReportIdentity("REPORT"),
            report=make_report(),
        )
    assert count(path) == 0


@pytest.mark.parametrize("revocation_first", [True, False])
def test_concurrent_revocation_serializes_with_report(
    tmp_path, monkeypatch, revocation_first,
):
    from threading import current_thread

    from sp001.infrastructure.retail_rule_evaluation_serialization import (
        serialize_retail_rule_evaluation_report,
    )

    path, grants, definitions, access, writer = environment(tmp_path)
    report = make_report()
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    first_acquired = Event()
    second_attempted = Event()
    release_first = Event()
    real_connect = sqlite3.connect

    class OrderedConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            is_begin = sql.strip().upper() == "BEGIN IMMEDIATE"
            name = current_thread().name
            if is_begin and name.startswith("second-operation"):
                second_attempted.set()

            result = super().execute(sql, parameters)

            if is_begin and name.startswith("first-operation"):
                first_acquired.set()
                if not release_first.wait(timeout=5):
                    raise TimeoutError("test did not release first transaction")
            return result

    def connect(*args, **kwargs):
        kwargs["factory"] = OrderedConnection
        return real_connect(*args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", connect)

    def revoke():
        return grants.apply(record=GrantAdministrationRecord(
            "CONCURRENT-REVOKE",
            access.principal,
            Action.REVOKE,
            definitions[0],
            150,
        ))

    def save():
        return writer.save_authorized(
            access=access, identity=identity, report=report,
        )

    first_operation = revoke if revocation_first else save
    second_operation = save if revocation_first else revoke

    with ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="first-operation"
    ) as first_executor, ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="second-operation"
    ) as second_executor:
        first_future = first_executor.submit(first_operation)
        try:
            assert first_acquired.wait(timeout=3)
            second_future = second_executor.submit(second_operation)
            assert second_attempted.wait(timeout=3)
            assert not first_future.done()
            assert not second_future.done()
        finally:
            release_first.set()

        if revocation_first:
            assert first_future.result(timeout=5) is True
            with pytest.raises(RetailReportAccessDenied):
                second_future.result(timeout=5)
        else:
            assert first_future.result(timeout=5) == report
            assert second_future.result(timeout=5) is True

    # Confirm that the actual administration path committed revocation + audit.
    snapshot = grants.read_grant_snapshot(grant_id=definitions[0].grant_id)
    assert snapshot is not None
    assert snapshot.revoked is True
    assert snapshot.revision == 2
    audit = grants.read_audit()
    assert len(audit) == 3
    assert audit[-1].event_id == "CONCURRENT-REVOKE"

    with sqlite3.connect(path) as connection:
        rows = connection.execute(
            "SELECT report_id, document "
            "FROM retail_rule_evaluation_reports"
        ).fetchall()

    if revocation_first:
        assert rows == []
    else:
        assert rows == [(
            identity.report_id,
            serialize_retail_rule_evaluation_report(report),
        )]

    # The current revocation also applies to an identical retry.
    with pytest.raises(RetailReportAccessDenied):
        writer.save_authorized(
            access=access, identity=identity, report=report,
        )

    assert count(path) == (0 if revocation_first else 1)


def test_authorized_recovery_uses_read_permission_only(tmp_path):
    from dataclasses import replace

    _, _, _, access, writer = environment(tmp_path)
    report = make_report()
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    writer.save_authorized(access=access, identity=identity, report=report)
    read_access = replace(
        access,
        permissions=tuple(
            permission for permission in access.permissions
            if permission.operation is Operation.READ_RETAIL_REPORT
        ),
    )
    assert writer.recover_authorized(
        access=read_access, identity=identity, case_id="CASE",
    ) == report
    assert writer.recover_authorized(
        access=read_access,
        identity=RetailRuleEvaluationReportIdentity("ABSENT"),
        case_id="CASE",
    ) is None


def test_revoked_read_grant_denies_existing_and_absent_reports(tmp_path):
    _, grants, definitions, access, writer = environment(tmp_path)
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    writer.save_authorized(
        access=access, identity=identity, report=make_report(),
    )
    assert grants.apply(record=GrantAdministrationRecord(
        "REVOKE-READ", access.principal, Action.REVOKE, definitions[1], 150,
    ))
    for requested in (identity, RetailRuleEvaluationReportIdentity("ABSENT")):
        with pytest.raises(RetailReportAccessDenied):
            writer.recover_authorized(
                access=access, identity=requested, case_id="CASE",
            )


def test_recovery_checks_actual_report_case(tmp_path):
    from dataclasses import replace

    _, grants, _, access, writer = environment(tmp_path)
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    writer.save_authorized(
        access=access, identity=identity, report=make_report(),
    )
    permission = CaseAccessPermission("OTHER-CASE", Operation.READ_RETAIL_REPORT)
    other_grant = CaseAccessGrant(
        "OTHER-GRANT", access.principal, permission, 100, 300,
    )
    assert grants.apply(record=GrantAdministrationRecord(
        "OTHER-EVENT", access.principal, Action.GRANT, other_grant, 100,
    ))
    other_access = replace(access, permissions=(permission,))
    with pytest.raises(RetailReportAccessDenied):
        writer.recover_authorized(
            access=other_access, identity=identity, case_id="OTHER-CASE",
        )


def test_recovery_expiry_before_return_rejects_and_closes_transaction(tmp_path):
    _, _, _, access, writer = environment(tmp_path)
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    report = make_report()
    writer.save_authorized(access=access, identity=identity, report=report)
    instants = iter((150, 200))
    reader = SqliteAuthorizedRetailReportWriter(
        database_path=tmp_path / "shared.sqlite3",
        expected_audience="REPORTS", clock=lambda: next(instants),
    )
    with pytest.raises(RetailReportAuthenticationRejected):
        reader.recover_authorized(
            access=access, identity=identity, case_id="CASE",
        )
    assert writer.recover_authorized(
        access=access, identity=identity, case_id="CASE",
    ) == report


def test_revocation_after_read_snapshot_is_observed_next_time(tmp_path):
    snapshot_established = Event()
    resume_read = Event()
    pause = [False]

    class ReadConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            if (
                pause[0]
                and sql.startswith(
                    "SELECT document FROM retail_rule_evaluation_reports"
                )
            ):
                snapshot_established.set()
                if not resume_read.wait(timeout=5):
                    raise TimeoutError("test did not resume snapshot read")
            return super().execute(sql, parameters)

    class Reader(SqliteAuthorizedRetailReportWriter):
        def _connect(self):
            connection = sqlite3.connect(
                self._path, timeout=5, isolation_level=None,
                factory=ReadConnection,
            )
            connection.execute("PRAGMA synchronous=FULL")
            return connection

    path, grants, definitions, access, writer = environment(tmp_path)
    report = make_report()
    identity = RetailRuleEvaluationReportIdentity("REPORT")
    writer.save_authorized(access=access, identity=identity, report=report)
    reader = Reader(
        database_path=path, expected_audience="REPORTS", clock=lambda: 150,
    )
    pause[0] = True

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            reader.recover_authorized,
            access=access, identity=identity, case_id="CASE",
        )
        try:
            assert snapshot_established.wait(timeout=3)
            assert not future.done()
            # WAL permits this committed revocation while the read retains
            # its already-established snapshot.
            assert grants.apply(record=GrantAdministrationRecord(
                "REVOKE-DURING-READ", access.principal,
                Action.REVOKE, definitions[1], 150,
            ))
        finally:
            resume_read.set()
        assert future.result(timeout=5) == report

    pause[0] = False
    with pytest.raises(RetailReportAccessDenied):
        reader.recover_authorized(
            access=access, identity=identity, case_id="CASE",
        )
    assert count(path) == 1
