import json
from dataclasses import replace
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)
from sp001.contracts.retail_rule_evaluation_admission import (
    RetailRuleEvaluationAdmission,
)
from sp001.infrastructure.retail_rule_evaluation_admission_serialization import (
    serialize_retail_rule_evaluation_admission as serialize,
    deserialize_retail_rule_evaluation_admission as deserialize,
)


def make_admission(fold=0):
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "Revisor VM"),
    )
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    evaluation = RetailRuleEvaluationRecord(
        "EVAL",
        RetailContextRuleObservation(
            "OBS", "RULE", "SNAPSHOT", 3, "CASE",
            RuleObservationStatus.NON_CONFORMANT, ("EVIDENCE",),
        ),
        RetailRuleCriterion("RULE", 2, "Criterio explícito."),
        actor,
        datetime(
            2025, 11, 2, 1, 30,
            tzinfo=ZoneInfo("America/New_York"), fold=fold,
        ),
        "Fundamento declarado; sin inferir aprobación.",
    )
    binding = RetailEvaluatorBinding(
        "BINDING", 7, principal, actor, "CASE", 100, 200,
    )
    return RetailRuleEvaluationAdmission(
        evaluation, principal,
        RetailEvaluatorBindingSnapshot(binding, False), 150,
    )


def dump(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


@pytest.mark.parametrize("fold", [0, 1])
def test_exact_roundtrip_preserves_full_content_and_named_timezone(fold):
    original = make_admission(fold)
    document = serialize(original)
    recovered = deserialize(document)
    assert recovered == original
    assert serialize(recovered) == document
    assert recovered.evaluation.evaluated_at.fold == fold
    assert recovered.evaluation.evaluated_at.tzinfo.key == "America/New_York"
    assert recovered.binding_snapshot.binding.revision == 7
    assert recovered.binding_snapshot.binding.actor == original.evaluation.evaluator
    assert recovered.validated_at == 150


@pytest.mark.parametrize("version", [2, True, "1", None])
def test_rejects_unknown_or_invalid_version(version):
    envelope = json.loads(serialize(make_admission()))
    envelope["schema_version"] = version
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


def test_rejects_duplicate_nested_key():
    document = serialize(make_admission()).replace(
        '"validated_at":150', '"validated_at":150,"validated_at":150',
    )
    with pytest.raises(ValueError, match="duplicate"):
        deserialize(document)


@pytest.mark.parametrize("location", ["envelope", "admission", "binding", "role"])
def test_rejects_additional_fields(location):
    envelope = json.loads(serialize(make_admission()))
    raw = envelope["admission"]
    targets = {
        "envelope": envelope,
        "admission": raw,
        "binding": raw["binding_snapshot"]["binding"],
        "role": raw["binding_snapshot"]["binding"]["actor"]["role"],
    }
    targets[location]["authority"] = "APPROVED"
    with pytest.raises(ValueError):
        deserialize(dump(envelope))


@pytest.mark.parametrize("mutation", [
    "principal", "role", "case", "revoked", "revision_bool",
    "validated_bool", "validated_expired",
])
def test_reexecutes_types_and_attribution_coherence(mutation):
    envelope = json.loads(serialize(make_admission()))
    raw = envelope["admission"]
    binding = raw["binding_snapshot"]["binding"]
    if mutation == "principal":
        raw["principal"]["subject"] = "OTHER"
    elif mutation == "role":
        binding["actor"]["role"]["role_id"] = "OTHER"
    elif mutation == "case":
        binding["case_id"] = "OTHER"
    elif mutation == "revoked":
        raw["binding_snapshot"]["revoked"] = True
    elif mutation == "revision_bool":
        binding["revision"] = True
    elif mutation == "validated_bool":
        raw["validated_at"] = True
    else:
        raw["validated_at"] = 200
    with pytest.raises((TypeError, ValueError)):
        deserialize(dump(envelope))


def test_historical_recovery_does_not_replace_binding_with_later_revocation():
    original = make_admission()
    document = serialize(original)
    later_snapshot = replace(
        original.binding_snapshot,
        binding=replace(original.binding_snapshot.binding, revision=8),
        revoked=True,
    )
    assert later_snapshot.revoked
    recovered = deserialize(document)
    assert recovered == original
    assert recovered.binding_snapshot.binding.revision == 7
    assert not recovered.binding_snapshot.revoked


@pytest.mark.parametrize("document", [
    "[]", "null", "{}",
    '{"schema_version":NaN,"admission":null}',
    '{"schema_version":1.0,"admission":null}',
])
def test_rejects_invalid_documents(document):
    with pytest.raises(ValueError):
        deserialize(document)


def test_rejects_noncanonical_format():
    with pytest.raises(ValueError, match="canonical"):
        deserialize(serialize(make_admission()) + "\n")


def test_requires_nominal_admission_and_string_document():
    with pytest.raises(TypeError):
        serialize(object())
    with pytest.raises(TypeError):
        deserialize(b"{}")
