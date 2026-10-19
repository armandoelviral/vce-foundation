from dataclasses import replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
    RetailRuleEvaluationReportIdentity,
    StoredRetailRuleEvaluationReport,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report as serialize,
    deserialize_retail_rule_evaluation_report as deserialize,
)
from sp001.infrastructure.sqlite_retail_rule_evaluation_reports import (
    SqliteRetailRuleEvaluationReportStore,
)
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)
from sp001.services.retail_rule_evaluation_persistence import (
    RetailRuleEvaluationPersistence,
)


def make_report():
    actor = RetailProcessActor(
        "ACTOR-TEST", "CUSTOMER-TEST", ActorType.HUMAN, "ORG-TEST",
        RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "VM reviewer"),
    )
    evaluation = RetailRuleEvaluationRecord(
        "EVAL-1",
        RetailContextRuleObservation(
            "OBS-1", "RULE-1", "SNAPSHOT-1", 1, "CASE-1",
            RuleObservationStatus.CONFORMANT, ("EVIDENCE-1",),
        ),
        RetailRuleCriterion("RULE-1", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic evaluation rationale.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE-1", evaluations=(evaluation,),
    )


def compose(store, **overrides):
    args = dict(store=store, serialize=serialize, deserialize=deserialize)
    args.update(overrides)
    return RetailRuleEvaluationPersistence(**args)


class FakeStore:
    def __init__(self, stored=None):
        self.stored = stored
        self.put_calls = 0

    def put(self, *, report):
        self.put_calls += 1
        return self.stored

    def get(self, *, identity):
        return self.stored


def test_save_retry_reopen_and_recover_real_sqlite(tmp_path):
    path = tmp_path / "reports.sqlite3"
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    report = make_report()
    service = compose(
        SqliteRetailRuleEvaluationReportStore(database_path=path)
    )
    assert service.save(identity=identity, report=report) == report
    assert service.save(identity=identity, report=report) == report

    reopened = compose(
        SqliteRetailRuleEvaluationReportStore(database_path=path)
    )
    assert reopened.recover(identity=identity) == report


def test_conflicting_save_preserves_original(tmp_path):
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    original = make_report()
    store = SqliteRetailRuleEvaluationReportStore(
        database_path=tmp_path / "reports.sqlite3"
    )
    service = compose(store)
    service.save(identity=identity, report=original)
    changed = replace(
        original,
        evaluations=(replace(
            original.evaluations[0], rationale="Different rationale."
        ),),
    )
    with pytest.raises(RetailRuleEvaluationReportConflict):
        service.save(identity=identity, report=changed)
    assert service.recover(identity=identity) == original


def test_absence_is_none():
    assert compose(FakeStore()).recover(
        identity=RetailRuleEvaluationReportIdentity("ABSENT")
    ) is None


def test_invalid_serialization_never_reaches_store():
    store = FakeStore()
    with pytest.raises(ValueError):
        compose(store, serialize=lambda report: "{}").save(
            identity=RetailRuleEvaluationReportIdentity("REPORT-1"),
            report=make_report(),
        )
    assert store.put_calls == 0


def test_lossy_serialization_never_reaches_store():
    report = make_report()
    changed = replace(
        report,
        evaluations=(replace(
            report.evaluations[0], rationale="Lost original rationale."
        ),),
    )
    store = FakeStore()
    with pytest.raises(ValueError, match="changes report"):
        compose(store, serialize=lambda value: serialize(changed)).save(
            identity=RetailRuleEvaluationReportIdentity("REPORT-1"),
            report=report,
        )
    assert store.put_calls == 0


@pytest.mark.parametrize("confirmation", [None, "invalid"])
def test_rejects_invalid_confirmation(confirmation):
    with pytest.raises(TypeError, match="confirmation"):
        compose(FakeStore(confirmation)).save(
            identity=RetailRuleEvaluationReportIdentity("REPORT-1"),
            report=make_report(),
        )


def test_rejects_different_confirmation():
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    wrong = StoredRetailRuleEvaluationReport(
        RetailRuleEvaluationReportIdentity("OTHER"),
        serialize(make_report()),
    )
    with pytest.raises(ValueError, match="confirmation differs"):
        compose(FakeStore(wrong)).save(
            identity=identity, report=make_report()
        )


def test_recovery_rejects_malformed_persisted_document():
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    store = FakeStore(StoredRetailRuleEvaluationReport(identity, "{}"))
    with pytest.raises(ValueError):
        compose(store).recover(identity=identity)


def test_recovery_rejects_wrong_identity():
    store = FakeStore(StoredRetailRuleEvaluationReport(
        RetailRuleEvaluationReportIdentity("OTHER"),
        serialize(make_report()),
    ))
    with pytest.raises(ValueError, match="different report identity"):
        compose(store).recover(
            identity=RetailRuleEvaluationReportIdentity("REPORT-1")
        )


def test_recovery_rejects_invalid_decoder_result():
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    store = FakeStore(StoredRetailRuleEvaluationReport(
        identity, serialize(make_report())
    ))
    with pytest.raises(TypeError, match="deserializer"):
        compose(store, deserialize=lambda document: None).recover(
            identity=identity
        )


def test_backend_failure_propagates():
    failure = OSError("synthetic backend failure")

    class BrokenStore(FakeStore):
        def get(self, *, identity):
            raise failure

        def put(self, *, report):
            raise failure

    service = compose(BrokenStore())
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    with pytest.raises(OSError) as caught:
        service.recover(identity=identity)
    assert caught.value is failure
    with pytest.raises(OSError) as caught:
        service.save(identity=identity, report=make_report())
    assert caught.value is failure
