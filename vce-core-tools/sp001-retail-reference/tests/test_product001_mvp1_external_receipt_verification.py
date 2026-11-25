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
