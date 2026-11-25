from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from hashlib import sha256
import json
import sqlite3
from threading import Barrier
from time import time

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.jwt_federated_issuance_authenticator import JwtFederatedIssuanceAuthenticator
from sp001.infrastructure.product001_mvp1_intelligence_lab import IntelligenceLabGate, mount_intelligence_lab


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def test_authenticated_intelligence_gate_consumes_once_before_observations(tmp_path):
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    signer = Ed25519PrivateKey.generate()
    now = int(time())
    resolver = ConfiguredAccessTokenKeys(issuer="issuer", public_keys={"token": rsa_key.public_key()})
    authenticator = JwtFederatedIssuanceAuthenticator(
        issuer="issuer", audience="audience", key_resolver=resolver,
        max_lifetime_seconds=300, max_token_bytes=8192,
    )
    database = tmp_path / "intelligence.sqlite"
    gate = IntelligenceLabGate(
        database_path=database, authenticator=authenticator, audience="audience",
        trust={"issuer": "issuer", "subject": "analyst", "signer_id": "analista-lab",
               "public_key_hex": signer.public_key().public_bytes_raw().hex()},
    )
    app = FastAPI()
    mount_intelligence_lab(app, gate)
    path = "/laboratory/vce/intelligence/version-checks"

    def headers(subject):
        token = jwt.encode(
            {"iss": "issuer", "aud": "audience", "sub": subject,
             "iat": now, "nbf": now, "exp": now + 120},
            rsa_key, algorithm="RS256", headers={"kid": "token", "typ": "at+jwt"},
        )
        return {"Authorization": "Bearer " + token}

    review = {
        "case_id": "VCE-INTEL-001", "revision": 1, "mode": "simulado",
        "scope": {"countries": ["México"]}, "configured_sources": ["F01"],
    }
    statement = {
        "domain": "VCE/INTELLIGENCE/LAB/VERSION-CHECK/V1", "case_id": "VCE-INTEL-001",
        "revision": 1, "review_sha256": sha256(canonical(review)).hexdigest(),
        "mode": "simulado", "action": "comprobar versiones",
        "signer_id": "analista-lab", "devices": ["EQ-01", "EQ-03"],
        "issued_at": now, "expires_at": now + 120,
    }
    payload = {
        "revision": review, "equipos": statement["devices"],
        "autorizacion": {"statement": statement, "signature_hex": signer.sign(canonical(statement)).hex()},
    }

    def counts():
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as db:
            return db.execute("""
                SELECT (SELECT count(*) FROM intelligence_consumption),
                       (SELECT count(*) FROM intelligence_observations)
            """).fetchone()

    with TestClient(app) as client:
        assert client.post(path, json=payload).status_code == 401
        assert client.post(path, json=payload, headers=headers("other")).status_code == 403
        assert client.post(
            path, json=payload | {"equipos": ["EQ-02"]}, headers=headers("analyst"),
        ).status_code == 403
        assert client.post(
            path, json=payload | {"revision": review | {"revision": 2}}, headers=headers("analyst"),
        ).status_code == 403
        assert counts() == (0, 0)

        with closing(sqlite3.connect(database)) as db:
            db.execute("""
                CREATE TRIGGER simulated_failure BEFORE INSERT ON intelligence_observations
                BEGIN SELECT RAISE(ABORT, 'simulated failure'); END
            """)
        assert client.post(path, json=payload, headers=headers("analyst")).status_code == 503
        assert counts() == (0, 0)
        with closing(sqlite3.connect(database)) as db:
            db.execute("DROP TRIGGER simulated_failure")

        barrier = Barrier(2)

        def submit():
            barrier.wait(timeout=5)
            return client.post(path, json=payload, headers=headers("analyst"))

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(submit) for _ in range(2)]
            responses = [future.result(timeout=8) for future in futures]
    assert sorted(response.status_code for response in responses) == [200, 409]
    accepted = next(response.json() for response in responses if response.status_code == 200)
    assert accepted["mode"] == "simulado"
    assert [row["device"] for row in accepted["observations"]] == ["EQ-01", "EQ-03"]
    assert counts() == (1, 2)
