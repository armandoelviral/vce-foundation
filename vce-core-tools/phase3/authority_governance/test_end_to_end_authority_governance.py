from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.authority_registry import (
    AuthorityRegistry,
)

from phase3.authority_governance.delegation_evaluation import (
    DelegationEvaluation,
)

from phase3.authority_governance.delegation_decision import (
    DelegationDecision,
)

from phase3.authority_governance.authority_query import (
    AuthorityQuery,
)

from phase3.authority_governance.authority_report import (
    AuthorityReport,
)

from phase3.authority_governance.authority_attestation import (
    AuthorityAttestation,
)


def test_end_to_end_authority_governance():

    registry = AuthorityRegistry()

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    registry.add(
        authority
    )

    evaluation = (
        DelegationEvaluation.evaluate(
            authority
        )
    )

    assert evaluation is True

    decision = (
        DelegationDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "DELEGATE"
    )

    query = AuthorityQuery(
        registry
    )

    recovered = query.by_id(
        "auth-001"
    )

    assert recovered == authority

    report = AuthorityReport(
        {
            "auth-001": recovered
        }
    )

    assert (
        report.authority_count()
        == 1
    )

    assert (
        report.authority_ids()
        == ["auth-001"]
    )

    attestation = (
        AuthorityAttestation.attest(
            attestation_id="att-001",
            authority=authority,
        )
    )

    assert (
        attestation.subject
        == "authority_record"
    )

    assert (
        attestation.evidence_hash
        == "auth-001"
    )
