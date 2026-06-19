from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)

from phase3.policy_versioning.policy_version_registry import (
    PolicyVersionRegistry,
)

from phase3.policy_versioning.version_change_evaluation import (
    VersionChangeEvaluation,
)

from phase3.policy_versioning.version_approval_decision import (
    VersionApprovalDecision,
)

from phase3.policy_versioning.policy_version_query import (
    PolicyVersionQuery,
)

from phase3.policy_versioning.policy_version_report import (
    PolicyVersionReport,
)

from phase3.policy_versioning.policy_version_attestation import (
    PolicyVersionAttestation,
)


def test_end_to_end_policy_version_governance():

    registry = PolicyVersionRegistry()

    version = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v2",
        approved_by="auth-001",
    )

    registry.add(version)

    evaluation = (
        VersionChangeEvaluation.evaluate(
            current_version="v1",
            proposed_version="v2",
        )
    )

    assert evaluation is True

    decision = (
        VersionApprovalDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "APPROVE_VERSION"
    )

    query = PolicyVersionQuery(
        registry
    )

    recovered = query.by_id(
        "trust-policy:v2"
    )

    assert recovered == version

    report = PolicyVersionReport(
        {
            "trust-policy:v2": recovered
        }
    )

    assert (
        report.version_count()
        == 1
    )

    assert (
        report.version_ids()
        == [
            "trust-policy:v2"
        ]
    )

    attestation = (
        PolicyVersionAttestation.attest(
            attestation_id="att-001",
            policy_version=version,
        )
    )

    assert (
        attestation.subject
        == "policy_version"
    )

    assert (
        attestation.evidence_hash
        == "trust-policy:v2"
    )
