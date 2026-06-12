from epics.epic082_external_ledger_root_anchoring.anchor_receipt import (
    AnchorReceipt,
)
from epics.epic082_external_ledger_root_anchoring.anchor_verifier import (
    verify_anchor_receipt,
)
from epics.epic082_external_ledger_root_anchoring.ledger_root import (
    LedgerRoot,
)


def build_root(
    root_hash="root-hash-001",
):

    return LedgerRoot(
        root_hash=root_hash,
        sequence_start=1,
        sequence_end=42,
        evidence_count=42,
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )


def build_receipt(
    root_hash="root-hash-001",
    status="ANCHORED",
):

    return AnchorReceipt(
        root_hash=root_hash,
        target_id="rekor",
        target_type="TRANSPARENCY_LOG",
        anchor_reference="rekor-log-index-001",
        anchored_at="2026-06-10T00:00:00Z",
        status=status,
    )


def test_anchor_verifier_accepts_matching_receipt():

    assert (
        verify_anchor_receipt(
            build_root(),
            build_receipt(),
        )
        is True
    )


def test_anchor_verifier_rejects_root_hash_mismatch():

    assert (
        verify_anchor_receipt(
            build_root(
                root_hash="root-hash-001"
            ),
            build_receipt(
                root_hash="root-hash-999"
            ),
        )
        is False
    )


def test_anchor_verifier_rejects_unanchored_status():

    assert (
        verify_anchor_receipt(
            build_root(),
            build_receipt(
                status="FAILED"
            ),
        )
        is False
    )
