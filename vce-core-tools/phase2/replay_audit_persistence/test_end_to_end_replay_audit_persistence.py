from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)

from phase2.replay_audit_persistence.replay_audit_store import (
    ReplayAuditStore,
)

from phase2.replay_audit_persistence.replay_audit_query import (
    ReplayAuditQuery,
)

from phase2.replay_audit_persistence.replay_comparator_result import (
    ReplayComparatorResult,
)

from phase2.replay_audit_persistence.replay_audit_verifier import (
    ReplayAuditVerifier,
)

from phase2.replay_audit_persistence.replay_audit_report import (
    ReplayAuditReport,
)

from phase2.replay_audit_persistence.replay_audit_attestation import (
    ReplayAuditAttestation,
)


def test_end_to_end_replay_audit_flow():

    store = ReplayAuditStore()

    audit = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    store.add(audit)

    query = ReplayAuditQuery(
        store
    )

    recovered = query.by_replay_id(
        "replay-001"
    )

    assert recovered.audit_result is True

    comparator = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    verified = (
        ReplayAuditVerifier.verify(
            comparator
        )
    )

    assert verified is True

    report = ReplayAuditReport(
        [recovered]
    )

    assert (
        report.total_audits()
        == 1
    )

    assert report.replay_ids() == [
        "replay-001"
    ]

    attestation = (
        ReplayAuditAttestation.attest(
            attestation_id="att-001",
            replay_audit=recovered,
        )
    )

    assert (
        attestation.subject
        == "replay_audit"
    )
