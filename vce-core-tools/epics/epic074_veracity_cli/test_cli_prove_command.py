import json

from epics.epic074_veracity_cli.veracity_cli import (
    run,
)


def test_cli_prove_returns_json_proof():

    output = run(
        [
            "prove",
        ]
    )

    payload = json.loads(
        output
    )

    assert payload["verified"] is True


def test_cli_prove_outputs_core_fields():

    output = run(
        [
            "prove",
        ]
    )

    payload = json.loads(
        output
    )

    assert "artifact_hash" in payload
    assert "ledger_sequence" in payload
    assert "verified" in payload
