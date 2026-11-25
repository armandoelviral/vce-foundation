from base64 import b64encode
from contextlib import closing
from dataclasses import asdict, replace
import json
import sqlite3

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_mvp1_authorization_eligibility import authorization_digest
from sp001.contracts.product001_mvp1_commitment_certificate import (
    commitment_certificate_digest,
    commitment_signing_payload,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1,
    authorization_signing_payload,
    decision_digest_from_canonical_bytes,
    documentary_binding_from_key,
)
from sp001.infrastructure.product001_mvp1_commercial_evidence import (
    CommercialEvidenceStatus,
    verify_commercial_evidence,
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
    database, _ = build_environment(tmp_path)
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
    clock = [150]

    def make_app(expected=certificate.context, *, verifier=None):
        _, reopened_service = build_environment(tmp_path, verifier=verifier)
        protected = compose_product001_mvp1_protected_approval(
            authenticated_service=reopened_service,
            commitment_admission=MVP1CommitmentAdmission(
                public_key=commitment_key.public_key(),
                resolve_context=lambda org, op: expected,
                clock=lambda: clock[0],
            ),
        )
        return create_product001_mvp1_http_app(
            protected_service=protected, enable_commitment_route=True,
        )

    def request_with(proof):
        return {
            "decision": json.loads(decision_bytes)["decision"],
            "certificate": {
                "version": 1,
                "context": asdict(proof.context),
                "signature_b64": b64encode(proof.signature).decode("ascii"),
            },
        }

    def sign_alternative():
        context = replace(certificate.context, authorization_digest="f" * 64)
        return replace(
            certificate, context=context,
            signature=commitment_key.sign(commitment_signing_payload(context)),
        )

    return (
        make_app, request_with, database, clock, certificate,
        sign_alternative, commitment_key.public_key(),
    )


def read_only_audit(database):
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as db:
        return db.execute(
            "SELECT sequence, decision_id, record FROM product001_commercial_decision_audit"
        ).fetchone()


def test_committed_certificate_records_once_over_http(committed_request):
    make_app, request_with, database, _, certificate, sign_alternative, _ = committed_request
    with TestClient(make_app()) as client:
        response = client.post(PATH, headers=HEADERS, json=request_with(certificate))
        assert response.status_code == 200, response.text
        assert response.json() == {"recorded": True}

    original = read_only_audit(database)
    _, decision_id, record = original
    assert decision_id == certificate.context.operation_id
    assert json.loads(record)["commitment"] == {
        "version": 1,
        "certificate_digest": commitment_certificate_digest(certificate),
        "context": asdict(certificate.context),
    }

    with TestClient(make_app()) as rebuilt_gate:
        response = rebuilt_gate.post(PATH, headers=HEADERS, json=request_with(certificate))
        assert response.json() == {"recorded": False}

    alternative = sign_alternative()
    with TestClient(make_app(alternative.context)) as configured_gate:
        response = configured_gate.post(PATH, headers=HEADERS, json=request_with(alternative))
        assert response.status_code == 409

    assert read_only_audit(database) == original
    assert decision_counts(database) == (1, 1)



def test_commitment_audit_rolls_back_with_decision(committed_request):
    make_app, request_with, database, _, certificate, _, _ = committed_request

    class RejectAtCommit:
        calls = 0

        def verify(self, *, decision):
            self.calls += 1
            if self.calls == 2:
                raise PermissionError("document changed before commit")

    verifier = RejectAtCommit()
    with TestClient(make_app(verifier=verifier)) as client:
        response = client.post(PATH, headers=HEADERS, json=request_with(certificate))
        assert response.status_code == 403
    assert verifier.calls == 2
    assert read_only_audit(database) is None
    assert decision_counts(database) == (0, 0)


def test_invalid_requests_leave_no_writes(committed_request):
    make_app, request_with, database, clock, certificate, _, _ = committed_request
    request = request_with(certificate)
    with TestClient(make_app()) as client:
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


def test_historical_evidence_is_verified_read_only(committed_request):
    make_app, request_with, database, clock, certificate, _, trusted_key = committed_request
    options = dict(
        database_path=database, certificate=certificate,
        trusted_key=trusted_key, trusted_issuer_id=certificate.context.issuer_id,
    )
    assert verify_commercial_evidence(**options) is CommercialEvidenceStatus.INDETERMINATE
    with TestClient(make_app()) as client:
        assert client.post(PATH, headers=HEADERS, json=request_with(certificate)).status_code == 200

    clock[0] = certificate.context.materialize_deadline
    original = read_only_audit(database)
    assert verify_commercial_evidence(**options) is CommercialEvidenceStatus.VERIFIED
    assert read_only_audit(database) == original
    assert decision_counts(database) == (1, 1)

    wrong_key = Ed25519PrivateKey.generate().public_key()
    assert verify_commercial_evidence(
        **(options | {"trusted_key": wrong_key})
    ) is CommercialEvidenceStatus.REJECTED
    missing_path = database.with_name("missing.sqlite")
    assert verify_commercial_evidence(
        **(options | {"database_path": missing_path})
    ) is CommercialEvidenceStatus.INDETERMINATE
    assert not missing_path.exists()


def test_absent_and_conflicting_commitment_references_are_distinct(committed_request):
    make_app, request_with, database, _, certificate, _, trusted_key = committed_request
    with TestClient(make_app()) as client:
        assert client.post(PATH, headers=HEADERS, json=request_with(certificate)).status_code == 200
    audit = json.loads(read_only_audit(database)[2])
    binding = audit.pop("commitment")
    options = dict(
        database_path=database, certificate=certificate,
        trusted_key=trusted_key, trusted_issuer_id=certificate.context.issuer_id,
    )
    for record, result in (
        (audit, CommercialEvidenceStatus.INDETERMINATE),
        (
            audit | {"commitment": binding | {"certificate_digest": "0" * 64}},
            CommercialEvidenceStatus.REJECTED,
        ),
    ):
        with closing(sqlite3.connect(database)) as db, db:
            db.execute(
                "UPDATE product001_commercial_decision_audit SET record = ?",
                (json.dumps(record, sort_keys=True, separators=(",", ":")),),
            )
        assert verify_commercial_evidence(**options) is result


def test_gate_receipt_recovers_committed_result_after_response_is_lost(committed_request):
    from hashlib import sha256

    from sp001.contracts.product001_mvp1_commercial_receipt import (
        CommercialReceiptV1,
        verify_commercial_receipt,
    )
    from sp001.services.product001_mvp1_commercial_receipt_issuer import (
        Mvp1CommercialReceiptIssuer,
    )

    make_app, request_with, database, clock, certificate, _, authority_key = committed_request
    signing_key = Ed25519PrivateKey.generate()
    options = dict(
        database_path=database,
        gate_id="gate-lab",
        signing_key=signing_key,
        trusted_issuer_id="issuer",
        trusted_authority_key=authority_key,
    )
    assert Mvp1CommercialReceiptIssuer(**options).recover(
        certificate,
    ) is CommercialEvidenceStatus.INDETERMINATE

    # Drop the delivery after the HTTP call commits and close the Gate instance.
    with TestClient(make_app()) as client:
        assert client.post(PATH, headers=HEADERS, json=request_with(certificate)).status_code == 200
    original = read_only_audit(database)

    clock[0] = certificate.context.materialize_deadline
    receipt = Mvp1CommercialReceiptIssuer(**options).recover(certificate)
    assert isinstance(receipt, CommercialReceiptV1)
    assert receipt == Mvp1CommercialReceiptIssuer(**options).recover(certificate)
    assert receipt.statement.audit_sequence == original[0]
    assert receipt.statement.audit_digest == sha256(original[2].encode("ascii")).hexdigest()
    verification = dict(
        certificate=certificate, trusted_gate_id="gate-lab",
        trusted_gate_key=signing_key.public_key(),
    )
    verify_commercial_receipt(receipt, **verification)
    with pytest.raises(PermissionError, match="invalid commercial receipt signature"):
        verify_commercial_receipt(
            replace(receipt, statement=replace(receipt.statement, audit_digest="0" * 64)),
            **verification,
        )
    with pytest.raises(PermissionError, match="invalid commercial receipt signature"):
        verify_commercial_receipt(receipt, **(
            verification | {"trusted_gate_key": Ed25519PrivateKey.generate().public_key()}
        ))
    assert read_only_audit(database) == original
    assert decision_counts(database) == (1, 1)
