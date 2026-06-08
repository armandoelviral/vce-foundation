import json

from epics.epic074_veracity_cli.veracity_cli import (
    run,
)


def test_cli_audit_returns_passed_status():

    output = run(
        [
            "audit",
        ]
    )

    payload = json.loads(
        output
    )

    assert payload["audit_status"] == "PASSED"
    assert payload["verified"] is True


def test_cli_audit_outputs_core_fields():

    output = run(
        [
            "audit",
        ]
    )

    payload = json.loads(
        output
    )

    assert "artifact_hash" in payload
    assert "ledger_sequence" in payload
    assert "audit_status" in payload
    assert "verified" in payload
