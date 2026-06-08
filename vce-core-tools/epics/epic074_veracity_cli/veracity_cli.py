import argparse
import json

from epics.epic073_veracity_sdk.veracity_runtime import (
    VeracityRuntime,
)


def build_parser():

    parser = argparse.ArgumentParser(
        prog="veracity",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "prove",
    )

    subparsers.add_parser(
        "verify",
    )

    return parser


def run(
    argv=None,
):

    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    runtime = VeracityRuntime()

    if args.command == "prove":

        proof = runtime.prove(
            identity={"identity_id": "cli-id"},
            trust={"certificate_id": "cli-cert"},
            provenance={"input_hash": "cli-input"},
            replay={"sequence_number": 3},
            evidence={"evidence_hash": "cli-evidence"},
            governance={"schema_version": "1.0"},
        )

        return runtime.export_proof(
            proof
        )

    if args.command == "verify":

        proof = runtime.prove(
            identity={"identity_id": "cli-id"},
            trust={"certificate_id": "cli-cert"},
            provenance={"input_hash": "cli-input"},
            replay={"sequence_number": 3},
            evidence={"evidence_hash": "cli-evidence"},
            governance={"schema_version": "1.0"},
        )

        payload = {
            "verified": runtime.verify(
                proof["artifact"],
                proof["receipt"],
            ),
            "artifact_hash": proof["receipt"].artifact_hash,
            "ledger_sequence": proof["receipt"].ledger_sequence,
        }

        return json.dumps(
            payload,
            sort_keys=True,
        )

    raise ValueError(
        f"Unknown command: {args.command}"
    )
