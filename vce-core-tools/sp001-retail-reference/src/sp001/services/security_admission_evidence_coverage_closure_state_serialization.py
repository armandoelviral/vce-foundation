import json

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)


SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION = 1


def serialize_security_admission_evidence_coverage_closure_state(
    *,
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> str:
    """Serialize one canonical coverage-closure state record to JSON."""

    if not isinstance(
        record,
        SecurityAdmissionEvidenceCoverageClosureStateRecord,
    ):
        raise TypeError(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        )

    resolution = record.closure_resolution
    coverage_identity = resolution.coverage_identity
    binding = (
        coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
    )
    evaluation_record = binding.evaluation_record
    evaluation_identity = evaluation_record.evaluation_identity
    evaluation_basis = evaluation_identity.evaluation_basis
    candidate_identity = evaluation_basis.candidate_identity
    requirements = binding.policy_evidence_requirements
    policy_identity = requirements.admission_policy_identity

    resolved_domain_count = sum(
        state.status
        is SecurityAdmissionEvidenceCoverageDomainClosureStatus.RESOLVED
        for state in record.domain_states
    )
    not_evaluated_domain_count = sum(
        state.status
        is SecurityAdmissionEvidenceCoverageDomainClosureStatus.NOT_EVALUATED
        for state in record.domain_states
    )
    impeded_domain = next(
        (
            state.domain.value
            for state in record.domain_states
            if state.status
            is SecurityAdmissionEvidenceCoverageDomainClosureStatus.IMPEDED
        ),
        None,
    )

    document = {
        "schema_version": (
            SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION
        ),
        "coverage_identity": {
            "coverage_id": coverage_identity.coverage_id,
            "coverage_version": coverage_identity.coverage_version,
            "evaluation_record": {
                "evaluation_id": evaluation_identity.evaluation_id,
                "evaluation_version": (
                    evaluation_identity.evaluation_version
                ),
                "evaluated_at": evaluation_record.evaluated_at.isoformat(),
                "candidate_identity": {
                    "candidate_id": candidate_identity.candidate_id,
                    "candidate_version": (
                        candidate_identity.candidate_version
                    ),
                    "customer_id": candidate_identity.customer_id,
                    "content_digest": {
                        "algorithm": (
                            candidate_identity.content_digest.algorithm
                        ),
                        "value": candidate_identity.content_digest.value,
                    },
                },
                "admission_policy_identity": {
                    "admission_policy_id": (
                        policy_identity.admission_policy_id
                    ),
                    "admission_policy_version": (
                        policy_identity.admission_policy_version
                    ),
                    "configuration_digest": {
                        "algorithm": (
                            policy_identity.configuration_digest.algorithm
                        ),
                        "value": (
                            policy_identity.configuration_digest.value
                        ),
                    },
                },
            },
            "required_evidence_domains": [
                domain.value
                for domain in requirements.required_evidence_domains
            ],
        },
        "terminal": {
            "kind": (
                "CLOSED"
                if isinstance(
                    resolution.outcome,
                    SecurityAdmissionEvidenceCoverageClosure,
                )
                else "BLOCKED"
            ),
            "resolved_domain_count": resolved_domain_count,
            "impeded_domain": impeded_domain,
            "not_evaluated_domain_count": (
                not_evaluated_domain_count
            ),
        },
        "domain_states": [
            {
                "domain": state.domain.value,
                "status": state.status.value,
            }
            for state in record.domain_states
        ],
    }

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
