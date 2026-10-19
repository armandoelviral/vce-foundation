import json
from dataclasses import fields
from datetime import datetime, timezone
from enum import Enum
from zoneinfo import ZoneInfo

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
    RetailRuleEvaluationReport,
)


_CLASSES = {
    cls.__name__: cls for cls in (
        RetailContextRuleObservation,
        RetailProcessRole,
        RetailProcessActor,
        RetailRuleCriterion,
        RetailRuleEvaluationRecord,
        RetailRuleEvaluationRelation,
        RetailRuleEvaluationReport,
    )
}
_ENUMS = {
    cls.__name__: cls for cls in (
        RuleObservationStatus,
        ActorType,
        RetailRuleEvaluationRelationType,
    )
}


def _encode(value):
    if type(value) in _ENUMS.values():
        return {"type": type(value).__name__, "value": value.value}
    if type(value) in (str, int):
        return value
    if type(value) is tuple:
        return {"type": "tuple", "items": [_encode(item) for item in value]}
    if type(value) is datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime must be timezone-aware")
        zone = None
        if isinstance(value.tzinfo, ZoneInfo):
            zone = value.tzinfo.key
        elif not isinstance(value.tzinfo, timezone):
            raise ValueError("unsupported timezone implementation")
        return {
            "type": "datetime",
            "iso": value.isoformat(),
            "fold": value.fold,
            "zone": zone,
        }
    if type(value) in _CLASSES.values():
        return {
            "type": type(value).__name__,
            "fields": {
                field.name: _encode(getattr(value, field.name))
                for field in fields(value)
            },
        }
    raise TypeError("unsupported value type")


def _exact_keys(value, expected):
    if set(value) != expected:
        raise ValueError("unexpected document fields")


def _decode(value):
    if type(value) in (str, int):
        return value
    if type(value) is not dict:
        raise ValueError("invalid encoded value")

    tag = value.get("type")
    if type(tag) is not str:
        raise ValueError("invalid type tag")

    if tag == "tuple":
        _exact_keys(value, {"type", "items"})
        if type(value["items"]) is not list:
            raise ValueError("tuple items must be a list")
        return tuple(_decode(item) for item in value["items"])

    if tag == "datetime":
        _exact_keys(value, {"type", "iso", "fold", "zone"})
        if type(value["iso"]) is not str:
            raise ValueError("invalid datetime text")
        if type(value["fold"]) is not int or value["fold"] not in (0, 1):
            raise ValueError("invalid datetime fold")
        parsed = datetime.fromisoformat(value["iso"])
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("datetime must be timezone-aware")
        zone = value["zone"]
        if zone is not None:
            if type(zone) is not str or not zone:
                raise ValueError("invalid timezone identity")
            parsed = parsed.astimezone(ZoneInfo(zone))
            if parsed.fold != value["fold"]:
                raise ValueError("timezone fold does not match encoded instant")
        else:
            parsed = parsed.replace(fold=value["fold"])
        if parsed.isoformat() != value["iso"]:
            raise ValueError("timezone rules do not match encoded offset")
        return parsed

    if tag in _ENUMS:
        _exact_keys(value, {"type", "value"})
        if type(value["value"]) is not str:
            raise ValueError("invalid enum value")
        return _ENUMS[tag](value["value"])

    if tag in _CLASSES:
        _exact_keys(value, {"type", "fields"})
        cls = _CLASSES[tag]
        raw = value["fields"]
        if type(raw) is not dict:
            raise ValueError("record fields must be an object")
        _exact_keys(raw, {field.name for field in fields(cls)})
        return cls(**{name: _decode(item) for name, item in raw.items()})

    raise ValueError("unknown type tag")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError("unsupported JSON number")


def serialize_retail_rule_evaluation_report(
    report: RetailRuleEvaluationReport,
) -> str:
    if type(report) is not RetailRuleEvaluationReport:
        raise TypeError("report must be a RetailRuleEvaluationReport")
    return json.dumps(
        {"schema_version": 1, "report": _encode(report)},
        sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def deserialize_retail_rule_evaluation_report(
    document: str,
) -> RetailRuleEvaluationReport:
    if type(document) is not str:
        raise TypeError("document must be a string")
    envelope = json.loads(
        document,
        object_pairs_hook=_unique_object,
        parse_float=_invalid_number,
        parse_constant=_invalid_number,
    )
    if type(envelope) is not dict:
        raise ValueError("envelope must be an object")
    _exact_keys(envelope, {"schema_version", "report"})
    if (
        type(envelope["schema_version"]) is not int
        or envelope["schema_version"] != 1
    ):
        raise ValueError("unsupported schema version")
    report = _decode(envelope["report"])
    if type(report) is not RetailRuleEvaluationReport:
        raise ValueError("root value must be a report")
    if serialize_retail_rule_evaluation_report(report) != document:
        raise ValueError("document must use canonical format")
    return report
