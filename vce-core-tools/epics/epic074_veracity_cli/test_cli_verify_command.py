import json

from epics.epic074_veracity_cli.veracity_cli import (
    run,
)


def test_cli_verify_returns_verified_true():

    output = run(
        [
            "verify",
        ]
    )

    payload = json.loads(
        output
    )

    assert payload["verified"] is True


def test_cli_verify_outputs_core_fields():

    output = run(
        [
            "verify",
        ]
    )

    payload = json.loads(
        output
    )

    assert "artifact_hash" in payload
    assert "ledger_sequence" in payload
    assert "verified" in payload
