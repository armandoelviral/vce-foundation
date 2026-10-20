import json
from dataclasses import asdict

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_evaluation_admission import (
    RetailRuleEvaluationAdmission,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report,
    deserialize_retail_rule_evaluation_report,
)
from sp001.services.retail_rule_evaluation_report import (
    RetailRuleEvaluationReport,
)


def _dump(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError("unsupported JSON number")


def _object(value, keys):
    if type(value) is not dict or set(value) != keys:
        raise ValueError("unexpected document fields")
    return value


def serialize_retail_rule_evaluation_admission(
    admission: RetailRuleEvaluationAdmission,
) -> str:
    """Encode declared admission content; establishes no authenticity."""
    if type(admission) is not RetailRuleEvaluationAdmission:
        raise TypeError("admission must be a RetailRuleEvaluationAdmission")
    evaluation = admission.evaluation
    report = RetailRuleEvaluationReport(
        case_id=evaluation.observation.case_id,
        evaluations=(evaluation,),
        relations=(),
    )
    return _dump({
        "schema_version": 1,
        "admission": {
            "evaluation_document": serialize_retail_rule_evaluation_report(report),
            "principal": asdict(admission.principal),
            "binding_snapshot": asdict(admission.binding_snapshot),
            "validated_at": admission.validated_at,
        },
    })


def deserialize_retail_rule_evaluation_admission(
    document: str,
) -> RetailRuleEvaluationAdmission:
    """Recover historical content without consulting current permissions."""
    if type(document) is not str:
        raise TypeError("document must be a string")
    envelope = json.loads(
        document, object_pairs_hook=_unique_object,
        parse_float=_invalid_number, parse_constant=_invalid_number,
    )
    _object(envelope, {"schema_version", "admission"})
    if (
        type(envelope["schema_version"]) is not int
        or envelope["schema_version"] != 1
    ):
        raise ValueError("unsupported schema version")
    raw = _object(envelope["admission"], {
        "evaluation_document", "principal", "binding_snapshot", "validated_at",
    })
    report = deserialize_retail_rule_evaluation_report(
        raw["evaluation_document"],
    )
    if len(report.evaluations) != 1 or report.relations:
        raise ValueError("admission must contain exactly one evaluation")

    principal = AuthenticatedPrincipal(**_object(
        raw["principal"], {"issuer", "subject"},
    ))
    snapshot = _object(raw["binding_snapshot"], {"binding", "revoked"})
    binding = _object(snapshot["binding"], {
        "binding_id", "revision", "principal", "actor",
        "case_id", "valid_from", "expires_at",
    })
    binding_principal = AuthenticatedPrincipal(**_object(
        binding["principal"], {"issuer", "subject"},
    ))
    actor = _object(binding["actor"], {
        "actor_id", "customer_id", "actor_type", "organization_id", "role",
    })
    role = RetailProcessRole(**_object(
        actor["role"], {"role_id", "customer_id", "role_name"},
    ))
    if type(actor["actor_type"]) is not str:
        raise ValueError("actor_type must be a string")
    restored_actor = RetailProcessActor(
        **{
            **actor,
            "actor_type": ActorType(actor["actor_type"]),
            "role": role,
        },
    )
    restored_binding = RetailEvaluatorBinding(**{
        **binding, "principal": binding_principal, "actor": restored_actor,
    })
    admission = RetailRuleEvaluationAdmission(
        evaluation=report.evaluations[0],
        principal=principal,
        binding_snapshot=RetailEvaluatorBindingSnapshot(
            binding=restored_binding, revoked=snapshot["revoked"],
        ),
        validated_at=raw["validated_at"],
    )
    if serialize_retail_rule_evaluation_admission(admission) != document:
        raise ValueError("document must use canonical format")
    return admission
