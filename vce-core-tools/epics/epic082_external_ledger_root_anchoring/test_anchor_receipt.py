from epics.epic082_external_ledger_root_anchoring.anchor_receipt import (
    AnchorReceipt,
)


def build_receipt():

    return AnchorReceipt(
        root_hash="root-hash-001",
        target_id="rekor",
        target_type="TRANSPARENCY_LOG",
        anchor_reference="rekor-log-index-001",
        anchored_at="2026-06-10T00:00:00Z",
        status="ANCHORED",
    )


def test_anchor_receipt_creation():

    receipt = build_receipt()

    assert receipt.root_hash == "root-hash-001"
    assert receipt.target_id == "rekor"
    assert receipt.status == "ANCHORED"


def test_anchor_receipt_contains_external_reference():

    receipt = build_receipt()

    assert receipt.anchor_reference == "rekor-log-index-001"


def test_anchor_receipt_serializes_to_dict():

    receipt = build_receipt()

    payload = receipt.to_dict()

    assert payload["root_hash"] == "root-hash-001"
    assert payload["target_id"] == "rekor"
    assert payload["target_type"] == "TRANSPARENCY_LOG"
    assert payload["anchor_reference"] == "rekor-log-index-001"
    assert payload["status"] == "ANCHORED"
