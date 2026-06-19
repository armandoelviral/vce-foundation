from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.governance_root_registry import (
    GovernanceRootRegistry,
)

from phase3.governance_merkle_root.root_evaluation import (
    RootEvaluation,
)

from phase3.governance_merkle_root.root_decision import (
    RootDecision,
)

from phase3.governance_merkle_root.root_query import (
    RootQuery,
)

from phase3.governance_merkle_root.root_report import (
    RootReport,
)

from phase3.governance_merkle_root.root_attestation import (
    RootAttestation,
)


def test_end_to_end_governance_merkle_root():

    registry = GovernanceRootRegistry()

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    registry.add(root)

    evaluation = RootEvaluation.evaluate(
        root
    )

    assert evaluation is True

    decision = RootDecision.from_evaluation(
        evaluation
    )

    assert (
        decision.status
        == "ACCEPT_ROOT"
    )

    query = RootQuery(
        registry
    )

    recovered = query.by_id(
        "root-001"
    )

    assert recovered == root

    report = RootReport(
        {
            "root-001": recovered
        }
    )

    assert report.root_count() == 1

    assert report.root_ids() == [
        "root-001"
    ]

    attestation = (
        RootAttestation.attest(
            attestation_id="att-001",
            root=root,
        )
    )

    assert (
        attestation.subject
        == "governance_merkle_root"
    )

    assert (
        attestation.evidence_hash
        == "root-001"
    )

