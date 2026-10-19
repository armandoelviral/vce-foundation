import sqlite3
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
            RuleObservationStatus.NON_CONFORMANT, ("EVIDENCE-1",),
        ),
        RetailRuleCriterion("RULE-1", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Original synthetic rationale.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE-1", evaluations=(evaluation,),
    )


def compose(store):
    return RetailRuleEvaluationPersistence(
        store=store, serialize=serialize, deserialize=deserialize,
    )


class LoseFirstConfirmation:
    def __init__(self, store):
        self.store = store
        self.confirmed_writes = 0
        self.failure = OSError("synthetic confirmation loss")

    def put(self, *, report):
        persisted = self.store.put(report=report)
        self.confirmed_writes += 1
        if self.confirmed_writes == 1:
            raise self.failure
        return persisted

    def get(self, *, identity):
        return self.store.get(identity=identity)


def assert_single_original_row(path, identity, document):
    with sqlite3.connect(path) as connection:
        rows = connection.execute(
            "SELECT report_id, document "
            "FROM retail_rule_evaluation_reports"
        ).fetchall()
    assert rows == [(identity.report_id, document)]


def test_lost_confirmation_recovery_and_retry_preserve_one_record(tmp_path):
    path = tmp_path / "reports.sqlite3"
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    original = make_report()
    document = serialize(original)
    adapter = SqliteRetailRuleEvaluationReportStore(database_path=path)
    failing_store = LoseFirstConfirmation(adapter)

    with pytest.raises(OSError) as caught:
        compose(failing_store).save(identity=identity, report=original)

    assert caught.value is failing_store.failure
    assert failing_store.confirmed_writes == 1
    assert_single_original_row(path, identity, document)

    reopened_adapter = SqliteRetailRuleEvaluationReportStore(
        database_path=path
    )
    reopened_service = compose(reopened_adapter)

    assert reopened_service.recover(identity=identity) == original
    assert reopened_service.save(identity=identity, report=original) == original
    assert reopened_service.recover(identity=identity) == original
    assert_single_original_row(path, identity, document)


def test_contradictory_retry_after_confirmation_loss_cannot_replace(tmp_path):
    path = tmp_path / "reports.sqlite3"
    identity = RetailRuleEvaluationReportIdentity("REPORT-1")
    original = make_report()
    document = serialize(original)
    failing_store = LoseFirstConfirmation(
        SqliteRetailRuleEvaluationReportStore(database_path=path)
    )

    with pytest.raises(OSError):
        compose(failing_store).save(identity=identity, report=original)

    changed = replace(
        original,
        evaluations=(replace(
            original.evaluations[0],
            rationale="Contradictory retry rationale.",
        ),),
    )
    service = compose(
        SqliteRetailRuleEvaluationReportStore(database_path=path)
    )
    with pytest.raises(RetailRuleEvaluationReportConflict):
        service.save(identity=identity, report=changed)

    assert service.recover(identity=identity) == original
    assert service.save(identity=identity, report=original) == original
    assert_single_original_row(path, identity, document)
