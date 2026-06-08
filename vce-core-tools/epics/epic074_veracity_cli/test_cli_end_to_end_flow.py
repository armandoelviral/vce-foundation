import json

from epics.epic074_veracity_cli.veracity_cli import (
    run,
)


def test_cli_end_to_end_flow():

    prove_output = run(
        ["prove"]
    )

    verify_output = run(
        ["verify"]
    )

    audit_output = run(
        ["audit"]
    )

    prove_payload = json.loads(
        prove_output
    )

    verify_payload = json.loads(
        verify_output
    )

    audit_payload = json.loads(
        audit_output
    )

    assert prove_payload["verified"] is True

    assert verify_payload["verified"] is True

    assert audit_payload["verified"] is True

    assert audit_payload["audit_status"] == "PASSED"


def test_cli_outputs_are_machine_readable():

    commands = [
        "prove",
        "verify",
        "audit",
    ]

    for command in commands:

        output = run(
            [command]
        )

        payload = json.loads(
            output
        )

        assert isinstance(
            payload,
            dict,
        )
