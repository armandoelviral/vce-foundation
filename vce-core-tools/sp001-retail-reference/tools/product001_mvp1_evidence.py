#!/usr/bin/env python3
"""Export and independently verify PRODUCT-001 commercial evidence."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_commercial_receipt import (
    CommercialReceiptStatementV1,
    CommercialReceiptV1,
)
from sp001.contracts.product001_mvp1_commitment_certificate import CommitmentContextV1
from sp001.infrastructure.product001_mvp1_commercial_evidence import (
    VerifiedCommercialAudit,
    read_verified_commercial_audit,
)
from sp001.infrastructure.product001_mvp1_http_codec import (
    _decode_signature,
    decode_product001_mvp1_commitment_certificate,
)
from sp001.infrastructure.product001_mvp1_http_json_parser import (
    MAX_PRODUCT001_MVP1_BODY_BYTES,
    parse_product001_mvp1_json_body,
)
from sp001.services.product001_mvp1_external_receipt_verification import (
    verify_exported_commercial_receipt,
)


def read_json(path, *, limit=MAX_PRODUCT001_MVP1_BODY_BYTES):
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("JSON file exceeds size limit")
    # The bundle can contain a JSON-escaped copy of the audit. Keep the
    # transport parser's original limit for each decoded component.
    if limit == MAX_PRODUCT001_MVP1_BODY_BYTES:
        return parse_product001_mvp1_json_body(data)
    value = json.loads(data)
    if data != (canonical_bundle(value) + "\n").encode("ascii"):
        raise ValueError("invalid canonical evidence bundle")
    return value


def canonical_bundle(bundle):
    return json.dumps(
        bundle, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    )


def decode_receipt(envelope):
    if set(envelope) != {"version", "statement", "signature_b64"}:
        raise ValueError("invalid receipt fields")
    if type(envelope["version"]) is not int or envelope["version"] != 1:
        raise ValueError("unsupported receipt version")
    statement = envelope["statement"].copy()
    statement["context"] = CommitmentContextV1(**statement["context"])
    return CommercialReceiptV1(
        CommercialReceiptStatementV1(**statement),
        _decode_signature(envelope["signature_b64"]),
    )


def public_key(path):
    with path.open("rb") as stream:
        raw = stream.read(128)
    return Ed25519PublicKey.from_public_bytes(bytes.fromhex(raw.decode("ascii").strip()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-key", type=Path, required=True, help="trusted public key in hex")
    parser.add_argument("--authority-key", type=Path, required=True, help="trusted public key in hex")
    parser.add_argument("--gate-id", required=True)
    parser.add_argument("--issuer-id", required=True)
    commands = parser.add_subparsers(dest="action", required=True)
    export = commands.add_parser("export")
    export.add_argument("--database", type=Path, required=True)
    export.add_argument("--certificate", type=Path, required=True)
    export.add_argument("--response", type=Path, required=True, help="HTTP response containing receipt")
    verify = commands.add_parser("verify")
    verify.add_argument("bundle", type=Path)
    args = parser.parse_args()

    try:
        gate_key = public_key(args.gate_key)
        authority_key = public_key(args.authority_key)
        if args.action == "export":
            certificate_wire = read_json(args.certificate)
            receipt_wire = read_json(args.response)["receipt"]
            certificate = decode_product001_mvp1_commitment_certificate(certificate_wire)
            audit = read_verified_commercial_audit(
                database_path=args.database, certificate=certificate,
                trusted_key=authority_key, trusted_issuer_id=args.issuer_id,
            )
            if not isinstance(audit, VerifiedCommercialAudit):
                raise PermissionError(f"commercial evidence: {audit.value}")
            bundle = {
                "version": 1,
                "certificate": certificate_wire,
                "receipt": receipt_wire,
                "audit": asdict(audit),
            }
        else:
            bundle = read_json(args.bundle, limit=8 * MAX_PRODUCT001_MVP1_BODY_BYTES)
            if set(bundle) != {"version", "certificate", "receipt", "audit"}:
                raise ValueError("invalid evidence bundle fields")
            if type(bundle["version"]) is not int or bundle["version"] != 1:
                raise ValueError("unsupported evidence bundle version")
            certificate = decode_product001_mvp1_commitment_certificate(bundle["certificate"])

        audit = bundle["audit"]
        if set(audit) != {"sequence", "canonical_record"}:
            raise ValueError("invalid audit fields")
        verify_exported_commercial_receipt(
            receipt=decode_receipt(bundle["receipt"]),
            certificate=certificate,
            audit_sequence=audit["sequence"],
            canonical_audit_record=audit["canonical_record"],
            trusted_gate_id=args.gate_id,
            trusted_gate_key=gate_key,
            trusted_issuer_id=args.issuer_id,
            trusted_authority_key=authority_key,
        )
    except (OSError, AttributeError, KeyError, TypeError, ValueError, RecursionError) as error:
        parser.exit(1, f"Evidence validation failed: {error}\n")

    if args.action == "export":
        serialized = canonical_bundle(bundle)
        if len(serialized) + 1 > 8 * MAX_PRODUCT001_MVP1_BODY_BYTES:
            parser.exit(1, "Evidence bundle exceeds size limit\n")
        print(serialized)
    else:
        print("VERIFIED")


if __name__ == "__main__":
    main()
