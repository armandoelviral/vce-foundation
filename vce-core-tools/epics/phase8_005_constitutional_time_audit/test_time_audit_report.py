from epics.phase8_005_constitutional_time_audit.time_audit_report import (
    generate_audit_report,
)


def test_generates_report():
    report = generate_audit_report(
        snapshot_id="snapshot.001",
        epoch=100,
    )

    assert report["snapshot_id"] == "snapshot.001"
    assert report["epoch"] == 100
