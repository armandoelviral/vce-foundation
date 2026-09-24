import ast
import inspect
import json

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_coverage_closure_state_projection import (
    project_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_serialization import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION,
    serialize_security_admission_evidence_coverage_closure_state,
)
from tests.test_security_admission_evidence_coverage_closure_resolution import (
    create_resolution,
)
from tests.test_security_admission_evidence_coverage_closure_state_record import (
    create_first_domain_blocked_resolution,
    create_second_domain_blocked_resolution,
)


Domain = SecurityAdmissionEvidenceDomain


def create_record(
    resolution_factory: object = create_resolution,
) -> SecurityAdmissionEvidenceCoverageClosureStateRecord:
    return project_security_admission_evidence_coverage_closure_state(
        resolution_factory()
    )


def serialize_record(
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> str:
    return serialize_security_admission_evidence_coverage_closure_state(
        record=record
    )


def test_schema_version_is_explicit() -> None:
    assert (
        SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION
        == 1
    )
    document = json.loads(serialize_record(create_record()))
    assert document["schema_version"] == 1


def test_complete_closure_serializes_closed_terminal() -> None:
    record = create_record()
    document = json.loads(serialize_record(record))
    assert document["terminal"] == {
        "kind": "CLOSED",
        "resolved_domain_count": len(record.domain_states),
        "impeded_domain": None,
        "not_evaluated_domain_count": 0,
    }
    assert all(
        state["status"] == "RESOLVED"
        for state in document["domain_states"]
    )


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_first_impediment_serializes_unevaluated_suffix(
    first_domain: Domain,
) -> None:
    record = create_record(
        lambda: create_first_domain_blocked_resolution(
            first_domain
        )
    )
    document = json.loads(serialize_record(record))
    assert document["terminal"] == {
        "kind": "BLOCKED",
        "resolved_domain_count": 0,
        "impeded_domain": first_domain.value,
        "not_evaluated_domain_count": 1,
    }
    assert document["domain_states"] == [
        {
            "domain": first_domain.value,
            "status": "IMPEDED",
        },
        {
            "domain": (
                Domain.BYTE_LENGTH.value
                if first_domain is Domain.MEDIA_TYPE
                else Domain.MEDIA_TYPE.value
            ),
            "status": "NOT_EVALUATED",
        },
    ]


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_second_impediment_serializes_resolved_prefix(
    first_domain: Domain,
) -> None:
    record = create_record(
        lambda: create_second_domain_blocked_resolution(
            first_domain
        )
    )
    document = json.loads(serialize_record(record))
    second_domain = (
        Domain.BYTE_LENGTH
        if first_domain is Domain.MEDIA_TYPE
        else Domain.MEDIA_TYPE
    )
    assert document["terminal"] == {
        "kind": "BLOCKED",
        "resolved_domain_count": 1,
        "impeded_domain": second_domain.value,
        "not_evaluated_domain_count": 0,
    }
    assert document["domain_states"] == [
        {
            "domain": first_domain.value,
            "status": "RESOLVED",
        },
        {
            "domain": second_domain.value,
            "status": "IMPEDED",
        },
    ]


def test_serialization_preserves_complete_identity_lineage() -> None:
    record = create_record()
    resolution = record.closure_resolution
    coverage = resolution.coverage_identity
    binding = (
        coverage
        .evaluation_record_policy_evidence_requirements_binding
    )
    evaluation = binding.evaluation_record
    evaluation_identity = evaluation.evaluation_identity
    candidate = (
        evaluation_identity
        .evaluation_basis
        .candidate_identity
    )
    policy = binding.policy_evidence_requirements.admission_policy_identity
    document = json.loads(serialize_record(record))
    serialized_coverage = document["coverage_identity"]
    serialized_evaluation = serialized_coverage["evaluation_record"]

    assert serialized_coverage["coverage_id"] == coverage.coverage_id
    assert (
        serialized_coverage["coverage_version"]
        == coverage.coverage_version
    )
    assert (
        serialized_evaluation["evaluation_id"]
        == evaluation_identity.evaluation_id
    )
    assert (
        serialized_evaluation["evaluation_version"]
        == evaluation_identity.evaluation_version
    )
    assert (
        serialized_evaluation["evaluated_at"]
        == evaluation.evaluated_at.isoformat()
    )
    assert serialized_evaluation["candidate_identity"] == {
        "candidate_id": candidate.candidate_id,
        "candidate_version": candidate.candidate_version,
        "customer_id": candidate.customer_id,
        "content_digest": {
            "algorithm": candidate.content_digest.algorithm,
            "value": candidate.content_digest.value,
        },
    }
    assert serialized_evaluation["admission_policy_identity"] == {
        "admission_policy_id": policy.admission_policy_id,
        "admission_policy_version": policy.admission_policy_version,
        "configuration_digest": {
            "algorithm": policy.configuration_digest.algorithm,
            "value": policy.configuration_digest.value,
        },
    }


@pytest.mark.parametrize(
    "resolution_factory",
    (
        create_resolution,
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        ),
        lambda: create_second_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        ),
    ),
)
def test_serialization_is_deterministic(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    first = serialize_record(record)
    second = serialize_record(record)
    assert first == second
    assert first.encode("UTF-8") == second.encode("UTF-8")


def test_serialization_is_sorted_and_compact() -> None:
    payload = serialize_record(create_record())
    assert payload == json.dumps(
        json.loads(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    assert "\n" not in payload
    assert ": " not in payload
    assert ", " not in payload


def test_required_domains_preserve_normative_order() -> None:
    record = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        )
    )
    document = json.loads(serialize_record(record))
    assert document["coverage_identity"][
        "required_evidence_domains"
    ] == [
        Domain.BYTE_LENGTH.value,
        Domain.MEDIA_TYPE.value,
    ]


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_record_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        ),
    ):
        serialize_security_admission_evidence_coverage_closure_state(
            record=invalid_value  # type: ignore[arg-type]
        )


def test_serialization_accepts_no_resolvers() -> None:
    signature = inspect.signature(
        serialize_security_admission_evidence_coverage_closure_state
    )
    assert tuple(signature.parameters) == ("record",)
    assert signature.parameters["record"].kind is inspect.Parameter.KEYWORD_ONLY


def test_serialization_has_no_assessment_or_decision_semantics() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state
    )
    forbidden = (
        "assessment",
        "classification",
        "admission_decision",
        "rejection",
        "authority",
        "resolver",
    )
    assert all(token not in source for token in forbidden)


def test_service_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        serialize_security_admission_evidence_coverage_closure_state
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert roots == {"sp001"}
    assert imports == {"json"}
