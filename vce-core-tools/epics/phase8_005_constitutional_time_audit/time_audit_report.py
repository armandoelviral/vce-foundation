def generate_audit_report(
    snapshot_id: str,
    epoch: int,
):
    return {
        "snapshot_id": snapshot_id,
        "epoch": epoch,
        "auditable": True,
    }
