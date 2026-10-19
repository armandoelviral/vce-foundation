import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

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
from sp001.contracts.retail_rule_evaluation_relation import (
    RetailRuleEvaluationRelation, RetailRuleEvaluationRelationType,
)
from sp001.services.retail_rule_evaluation_report import (
    build_retail_rule_evaluation_report,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report as serialize,
    deserialize_retail_rule_evaluation_report as deserialize,
)


def make_report():
    actor = RetailProcessActor(
        "ACTOR-TEST", "CUSTOMER-TEST", ActorType.HUMAN, "ORG-TEST",
        RetailProcessRole("ROLE-TEST", "CUSTOMER-TEST", "Revisor VM"),
    )
    first = RetailRuleEvaluationRecord(
        "EVAL-1",
        RetailContextRuleObservation(
            "OBS-1", "RULE-1", "SNAPSHOT-1", 1, "CASE-1",
            RuleObservationStatus.NON_CONFORMANT, ("EVIDENCE-1",),
        ),
        RetailRuleCriterion("RULE-1", 1, "Criterio sintético explícito."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Fundamento inicial; sin inferir aprobación.",
    )
    second = replace(
        first, evaluation_id="EVAL-2",
        criterion=RetailRuleCriterion("RULE-1", 2, "Criterio revisado."),
        evaluated_at=first.evaluated_at + timedelta(seconds=1),
        rationale="Revisión del juicio bajo otro criterio.",
    )
    relation = RetailRuleEvaluationRelation(
        "REL-1", first, second,
        RetailRuleEvaluationRelationType.JUDGMENT_REVIEW,
        "Relación declarada; no causal.",
    )
    return build_retail_rule_evaluation_report(
        case_id="CASE-1",
        evaluations=(first, second),
        relations=(relation,),
    )


def dump(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def test_roundtrip_preserves_full_report_and_deterministic_document():
    original = make_report()
    document = serialize(original)
    recovered = deserialize(document)
    assert recovered == original
    assert serialize(recovered) == document
    assert recovered.evaluations[0].rationale == (
        "Fundamento inicial; sin inferir aprobación."
    )
    assert recovered.evaluations[1].criterion.criterion_version == 2
    assert recovered.relations[0].previous == recovered.evaluations[0]
    assert recovered.evaluations[0].evaluator == original.evaluations[0].evaluator


@pytest.mark.parametrize("zone", [
    timezone(timedelta(hours=-6)),
    ZoneInfo("America/Mexico_City"),
])
def test_preserves_time_offset_and_named_zone(zone):
    original = make_report()
    record = replace(
        original.evaluations[0],
        evaluated_at=datetime(2026, 1, 1, 12, 30, tzinfo=zone),
    )
    report = build_retail_rule_evaluation_report(
        case_id="CASE-1", evaluations=(record,),
    )
    recovered = deserialize(serialize(report))
    assert recovered == report
    assert recovered.evaluations[0].evaluated_at.isoformat() == (
        record.evaluated_at.isoformat()
    )
    if isinstance(zone, ZoneInfo):
        assert recovered.evaluations[0].evaluated_at.tzinfo.key == zone.key


@pytest.mark.parametrize("fold", [0, 1])
def test_preserves_ambiguous_named_zone_time(fold):
    original = make_report()
    record = replace(
        original.evaluations[0],
        evaluated_at=datetime(
            2025, 11, 2, 1, 30, tzinfo=ZoneInfo("America/New_York"),
            fold=fold,
        ),
    )
    report = build_retail_rule_evaluation_report(
        case_id="CASE-1", evaluations=(record,),
    )
    recovered = deserialize(serialize(report))
    assert recovered.evaluations[0].evaluated_at.fold == fold
    assert serialize(recovered) == serialize(report)


@pytest.mark.parametrize("version", [2, True, "1", None])
def test_rejects_unknown_or_invalid_schema_version(version):
    envelope = json.loads(serialize(make_report()))
    envelope["schema_version"] = version
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


def test_rejects_duplicate_keys():
    document = serialize(make_report())
    document = document.replace(
        '"schema_version":1', '"schema_version":1,"schema_version":1'
    )
    with pytest.raises(ValueError, match="duplicate"):
        deserialize(document)


def test_rejects_unknown_field():
    envelope = json.loads(serialize(make_report()))
    envelope["report"]["fields"]["authority"] = "APPROVED"
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


def test_rejects_unknown_type():
    envelope = json.loads(serialize(make_report()))
    envelope["report"]["type"] = "UnregisteredType"
    with pytest.raises(ValueError, match="unknown type"):
        deserialize(dump(envelope))


def test_reexecutes_reference_validation_on_recovery():
    envelope = json.loads(serialize(make_report()))
    records = envelope["report"]["fields"]["evaluations"]["items"]
    records[1]["fields"]["rationale"] = "Conflicting embedded evaluation."
    with pytest.raises(ValueError, match="content conflicts"):
        deserialize(dump(envelope))


def test_reexecutes_nominal_validation_on_recovery():
    envelope = json.loads(serialize(make_report()))
    records = envelope["report"]["fields"]["evaluations"]["items"]
    records[0]["fields"]["rationale"] = ""
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


@pytest.mark.parametrize("document", [
    "[]", "null", "{}", '{"schema_version":NaN,"report":null}',
    '{"schema_version":1.0,"report":null}',
])
def test_rejects_invalid_documents(document):
    with pytest.raises(ValueError):
        deserialize(document)


def test_rejects_noncanonical_whitespace():
    document = serialize(make_report())
    with pytest.raises(ValueError, match="canonical"):
        deserialize(document + "\n")


def test_rejects_non_report_root():
    envelope = json.loads(serialize(make_report()))
    envelope["report"] = "not a report"
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


def test_requires_string_document():
    with pytest.raises(TypeError):
        deserialize(b"{}")
