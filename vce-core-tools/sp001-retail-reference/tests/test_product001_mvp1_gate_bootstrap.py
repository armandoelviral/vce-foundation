from dataclasses import asdict
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from sp001.contracts.product001_mvp1_commitment_certificate import CommitmentContextV1
from sp001.infrastructure.product001_mvp1_gate_bootstrap import (
    _read_trust_configuration,
    create_product001_mvp1_deployed_gate,
)

from test_authenticated_product001_commercial_document_integration import build_environment


@pytest.fixture
def startup(tmp_path):
    uid = os.geteuid()
    if uid == 0:
        pytest.skip("requires an unprivileged Gate account")
    _, service = build_environment(tmp_path)
    configuration = {
        "commitment_public_key_hex": (
            Ed25519PrivateKey.generate().public_key().public_bytes_raw().hex()
        ),
        "commitments": [asdict(CommitmentContextV1(
            issuer_id="issuer", organization_id="org", operation_id="operation",
            authorization_digest="a" * 64, decision_digest="b" * 64,
            materialize_deadline=4_000_000_000,
        ))],
    }
    with TemporaryDirectory(dir=Path.home().resolve()) as directory:
        path = Path(directory) / "trust.json"
        path.write_text(json.dumps(configuration), encoding="utf-8")
        path.chmod(0o600)
        yield path, uid + 1, service, configuration


def start(path, uid, service):
    return create_product001_mvp1_deployed_gate(
        authenticated_service=service,
        trust_configuration_path=path,
        commercial_uid=uid,
    )


def test_protected_configuration_enables_only_certificate_route(startup):
    path, uid, service, _ = startup
    app = start(path, uid, service)
    with TestClient(app) as client:
        route = "/laboratory/product001/mvp1/decisions"
        assert client.post(route, json={}).status_code == 401
        assert client.post(
            route, headers={"Authorization": "Bearer valid"},
            json={"decision": {}, "certificate": {"signature_b64": ""}},
        ).status_code == 400
        assert client.get("/openapi.json").status_code == 404


def test_startup_rejects_same_account(startup):
    path, _, service, _ = startup
    with pytest.raises(PermissionError, match="distinct unprivileged accounts"):
        start(path, os.geteuid(), service)


@pytest.mark.parametrize("permission_target", ["file", "directory"])
def test_startup_rejects_writable_trust_paths(startup, permission_target):
    path, uid, service, _ = startup
    target = path if permission_target == "file" else path.parent
    target.chmod(0o770 if permission_target == "directory" else 0o660)
    with pytest.raises(PermissionError, match="unsafe Gate trust"):
        start(path, uid, service)


def test_startup_rejects_symbolic_link(startup):
    path, _, _, _ = startup
    link = path.with_name("link.json")
    link.symlink_to(path.name)
    with pytest.raises(OSError):
        _read_trust_configuration(link, gate_uid=os.geteuid())


def test_startup_rejects_ambiguous_context(startup):
    path, uid, service, configuration = startup
    configuration["commitments"] *= 2
    path.write_text(json.dumps(configuration), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate trusted commitment identity"):
        start(path, uid, service)
