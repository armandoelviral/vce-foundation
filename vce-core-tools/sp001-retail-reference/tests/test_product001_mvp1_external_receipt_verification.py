from dataclasses import replace

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from sp001.services.product001_mvp1_commercial_receipt_issuer import Mvp1CommercialReceiptIssuer
from sp001.services.product001_mvp1_external_receipt_verification import (
    verify_exported_commercial_receipt,
)
from test_product001_mvp1_http_commitment_route import HEADERS, PATH, committed_request, read_only_audit


def test_external_verification_and_substitutions(committed_request):
    make_app, request_with, database, _, certificate, alternative, authority_key = committed_request
    gate_key = Ed25519PrivateKey.generate()
    with TestClient(make_app()) as client:
        assert client.post(PATH, headers=HEADERS, json=request_with(certificate)).status_code == 200
    sequence, _, audit = read_only_audit(database)
    receipt = Mvp1CommercialReceiptIssuer(
        database_path=database, gate_id="gate", signing_key=gate_key,
        trusted_issuer_id=certificate.context.issuer_id, trusted_authority_key=authority_key,
    ).recover(certificate)
    options = dict(
        receipt=receipt, certificate=certificate, audit_sequence=sequence,
        canonical_audit_record=audit, trusted_gate_id="gate",
        trusted_gate_key=gate_key.public_key(), trusted_authority_key=authority_key,
        trusted_issuer_id=certificate.context.issuer_id,
    )
    verify_exported_commercial_receipt(**options)
    for changed in (
        {"receipt": replace(receipt, signature=bytes(64))},
        {"certificate": alternative()},
        {"canonical_audit_record": audit + " "},
        {"audit_sequence": sequence + 1},
        {"trusted_authority_key": gate_key.public_key()},
        {"trusted_gate_key": authority_key},
    ):
        with pytest.raises(PermissionError):
            verify_exported_commercial_receipt(**(options | changed))


def test_evidence_command_exports_reproducibly_and_verifies_offline(committed_request, tmp_path):
    from base64 import b64encode
    import json
    from pathlib import Path
    import subprocess
    import sys

    make_app, request_with, database, _, certificate, _, authority_key = committed_request
    gate_key = Ed25519PrivateKey.generate()
    issuer = Mvp1CommercialReceiptIssuer(
        database_path=database, gate_id="gate", signing_key=gate_key,
        trusted_issuer_id=certificate.context.issuer_id, trusted_authority_key=authority_key,
    )
    request = request_with(certificate)
    with TestClient(make_app(receipt_issuer=issuer)) as client:
        response = client.post(PATH, headers=HEADERS, json=request)
        assert response.status_code == 200
    (tmp_path / "certificate.json").write_text(json.dumps(request["certificate"]))
    (tmp_path / "response.json").write_bytes(response.content)
    (tmp_path / "gate.pub").write_text(gate_key.public_key().public_bytes_raw().hex())
    (tmp_path / "authority.pub").write_text(authority_key.public_bytes_raw().hex())

    tool = Path(__file__).resolve().parents[1] / "tools/product001_mvp1_evidence.py"
    command = [
        sys.executable, str(tool), "--gate-id", "gate",
        "--issuer-id", certificate.context.issuer_id,
        "--gate-key", "gate.pub", "--authority-key", "authority.pub",
    ]
    export = ["export", "--database", str(database),
              "--certificate", "certificate.json", "--response", "response.json"]
    original = subprocess.check_output(command + export, cwd=tmp_path)
    assert original == subprocess.check_output(command + export, cwd=tmp_path)
    portable = tmp_path / "portable"
    portable.mkdir()
    for name in ("gate.pub", "authority.pub"):
        (portable / name).write_bytes((tmp_path / name).read_bytes())
    bundle = portable / "evidence.json"
    bundle.write_bytes(original)
    verify = command + ["verify", bundle.name]
    assert subprocess.check_output(verify, cwd=portable) == b"VERIFIED\n"

    for field in ("certificate", "receipt", "audit"):
        evidence = json.loads(original)
        if field == "audit":
            evidence[field]["sequence"] += 1
        else:
            evidence[field]["signature_b64"] = b64encode(bytes(64)).decode("ascii")
        bundle.write_text(json.dumps(evidence, sort_keys=True, separators=(",", ":")) + "\n")
        failure = subprocess.run(verify, cwd=portable, capture_output=True)
        assert failure.returncode == 1
        assert failure.stdout == b""
