from epics.epic082_external_ledger_root_anchoring.anchor_receipt import (
    AnchorReceipt,
)
from epics.epic082_external_ledger_root_anchoring.anchor_target_registry import (
    AnchorTarget,
    AnchorTargetRegistry,
)
from epics.epic082_external_ledger_root_anchoring.anchor_verifier import (
    verify_anchor_receipt,
)
from epics.epic082_external_ledger_root_anchoring.root_generator import (
    generate_ledger_root,
)


def test_end_to_end_external_anchoring_flow():

    evidence_records = [
        {
            "sequence": 1,
            "artifact_hash": "artifact-001",
            "admission_status": "ADMITTED",
        },
        {
            "sequence": 2,
            "artifact_hash": "artifact-002",
            "admission_status": "ADMITTED",
        },
    ]

    ledger_root = generate_ledger_root(
        evidence_records=evidence_records,
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    registry = AnchorTargetRegistry()

    registry.register(
        AnchorTarget(
            target_id="rekor",
            target_type="TRANSPARENCY_LOG",
            active=True,
        )
    )

    active_targets = registry.active_targets()

    assert len(active_targets) == 1

    target = active_targets[0]

    receipt = AnchorReceipt(
        root_hash=ledger_root.root_hash,
        target_id=target.target_id,
        target_type=target.target_type,
        anchor_reference="rekor-log-index-001",
        anchored_at="2026-06-10T00:01:00Z",
        status="ANCHORED",
    )

    assert verify_anchor_receipt(
        ledger_root,
        receipt,
    ) is True

    assert receipt.target_id == "rekor"
    assert receipt.status == "ANCHORED"


def test_end_to_end_external_anchoring_rejects_wrong_receipt():

    evidence_records = [
        {
            "sequence": 1,
            "artifact_hash": "artifact-001",
            "admission_status": "ADMITTED",
        }
    ]

    ledger_root = generate_ledger_root(
        evidence_records=evidence_records,
        region="us-east-1",
        generated_at="2026-06-10T00:00:00Z",
    )

    forged_receipt = AnchorReceipt(
        root_hash="forged-root-hash",
        target_id="rekor",
        target_type="TRANSPARENCY_LOG",
        anchor_reference="rekor-log-index-999",
        anchored_at="2026-06-10T00:01:00Z",
        status="ANCHORED",
    )

    assert verify_anchor_receipt(
        ledger_root,
        forged_receipt,
    ) is False
