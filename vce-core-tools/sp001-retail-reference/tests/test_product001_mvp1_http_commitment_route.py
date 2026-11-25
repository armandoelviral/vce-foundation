from base64 import b64encode
from dataclasses import asdict, replace
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_mvp1_authorization_eligibility import authorization_digest
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1,
    authorization_signing_payload,
    decision_digest_from_canonical_bytes,
    documentary_binding_from_key,
)
from sp001.infrastructure.product001_mvp1_http_host import create_product001_mvp1_http_app
from sp001.infrastructure.product001_mvp1_protected_composition import (
    compose_product001_mvp1_protected_approval,
)
from sp001.infrastructure.sqlite_product001_mvp1_authorization_store import (
    SqliteMvp1AuthorizationStore,
)
from sp001.services.product001_mvp1_commitment_issuer import Mvp1CommitmentIssuer
from sp001.services.product001_mvp1_execution_gate import (
    MVP1CommitmentAdmission,
    authorization_payload,
)

from test_authenticated_product001_commercial_document_integration import (
    build_environment,
    decision_counts,
    publish,
)
from test_product001_commercial_document_verification import matching_decision


PATH = "/laboratory/product001/mvp1/decisions"
HEADERS = {"Authorization": "Bearer valid"}


@pytest.fixture
def committed_request(tmp_path):
    decision = matching_decision()
    publish(tmp_path, decision)
    database, authenticated = build_environment(tmp_path)
    document = Product001DocumentaryCommitmentKey(
        organization_id=decision.document_scope.organization_id,
        source_identity=decision.document_identity,
    )
    decision_bytes = authorization_payload(decision)
    approval_key = Ed25519PrivateKey.generate()
    commitment_key = Ed25519PrivateKey.generate()
    unsigned = ContextualAuthorizationV1(
        operation_id=decision.decision_id,
        decision_digest=decision_digest_from_canonical_bytes(decision_bytes),
        issuer_id="issuer",
        authority_sequence=1,
        materialize_deadline=160,
        documentary_binding=documentary_binding_from_key(document),
        signature=bytes(64),
    )
    authorization = replace(
        unsigned, signature=approval_key.sign(authorization_signing_payload(unsigned)),
    )
    store = SqliteMvp1AuthorizationStore(
        database_path=tmp_path / "authority.sqlite",
        issuer_id="issuer", public_key=approval_key.public_key(), clock=lambda: 150,
    )
    context = dict(
        operation_id=decision.decision_id, decision_bytes=decision_bytes,
        documentary_key=document,
    )
    store.register(authorization, **context)
    store.consume(authorization, **context)
    certificate = Mvp1CommitmentIssuer(store=store, signing_key=commitment_key).issue(
        organization_id=document.organization_id, operation_id=decision.decision_id,
        authorization_digest=authorization_digest(authorization),
    )
    expected = {(document.organization_id, decision.decision_id): certificate.context}
    clock = [150]
    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated,
        commitment_admission=MVP1CommitmentAdmission(
            public_key=commitment_key.public_key(),
            resolve_context=lambda org, op: expected.get((org, op)),
            clock=lambda: clock[0],
        ),
    )
    request = {
        "decision": json.loads(decision_bytes)["decision"],
        "certificate": {
            "version": 1,
            "context": asdict(certificate.context),
            "signature_b64": b64encode(certificate.signature).decode("ascii"),
        },
    }
    app = create_product001_mvp1_http_app(
        protected_service=protected, enable_commitment_route=True,
    )
    return app, request, database, clock


def test_committed_certificate_records_once_over_http(committed_request):
    app, request, database, _ = committed_request
    with TestClient(app) as client:
        for recorded in (True, False):
            response = client.post(PATH, headers=HEADERS, json=request)
            assert response.status_code == 200, response.text
            assert response.json() == {"recorded": recorded}
    assert decision_counts(database) == (1, 1)


def test_invalid_requests_leave_no_writes(committed_request):
    app, request, database, clock = committed_request
    with TestClient(app) as client:
        assert client.post(PATH, json=request).status_code == 401
        changed = request | {"decision": request["decision"] | {"evidence_reference": "other"}}
        assert client.post(PATH, headers=HEADERS, json=changed).status_code == 403
        legacy = {"signature_b64": request["certificate"]["signature_b64"]}
        assert client.post(
            PATH, headers=HEADERS, json=request | {"certificate": legacy},
        ).status_code == 400
        assert client.post(
            PATH, headers=HEADERS, content=b" " * 65_537,
        ).status_code == 400
        clock[0] = 160
        assert client.post(PATH, headers=HEADERS, json=request).status_code == 403
    assert decision_counts(database) == (0, 0)


def test_opt_in_requires_commitment_mode(tmp_path):
    _, authenticated = build_environment(tmp_path)
    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated,
        authority_public_key=Ed25519PrivateKey.generate().public_key(),
    )
    with pytest.raises(ValueError, match="requires certificate admission"):
        create_product001_mvp1_http_app(
            protected_service=protected, enable_commitment_route=True,
        )
