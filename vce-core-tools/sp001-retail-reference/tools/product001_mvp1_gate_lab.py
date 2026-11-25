#!/usr/bin/env python3
"""Provision and serve an isolated PRODUCT-001 launchd pilot."""

import argparse
from base64 import b64encode
from contextlib import closing
from dataclasses import asdict, replace
import json
import os
import sqlite3
from pathlib import Path
import sys
from time import time

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

import jwt
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)

from sp001.contracts.product001_documentary_commitment import Product001DocumentaryCommitmentKey
from sp001.contracts.product001_mvp1_authorization_eligibility import authorization_digest
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1,
    authorization_signing_payload,
    decision_digest_from_canonical_bytes,
    documentary_binding_from_key,
)
from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.product001_commercial_approval_composition import (
    compose_product001_commercial_approval,
)
from sp001.infrastructure.product001_mvp1_gate_bootstrap import (
    GateReceiptConfiguration,
    create_product001_mvp1_deployed_gate,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    SqliteProduct001CommercialDecisionWriter,
)
from sp001.infrastructure.sqlite_product001_mvp1_authorization_store import (
    SqliteMvp1AuthorizationStore,
)
from sp001.services.product001_mvp1_commitment_issuer import Mvp1CommitmentIssuer
from sp001.services.product001_mvp1_execution_gate import authorization_payload

ISSUER = "sp001-lab"
AUDIENCE = "sp001-commercial-lab"
KEY_ID = "sp001-lab-rs256"
INTERRUPTED_AFTER_COMMIT = 75
CREDENTIAL_TTL_SECONDS = 600
PORT = 18766
ROUTE = "/laboratory/product001/mvp1/decisions"


def provision(
    state: Path,
    *,
    authority_state: Path | None = None,
    interrupt: bool = False,
    commitment_ttl_seconds: int = CREDENTIAL_TTL_SECONDS,
    revocation_order: str | None = None,
) -> None:
    # Fixture imports are only needed during provisioning.
    sys.path.insert(0, str(PROJECT / "tests"))
    from test_authenticated_product001_commercial_approval import grant
    from test_authenticated_product001_commercial_document_integration import publish
    from test_product001_commercial_document_verification import matching_decision

    state.mkdir(mode=0o700)
    now = int(time())
    credential_deadline = now + CREDENTIAL_TTL_SECONDS
    commitment_deadline = now + commitment_ttl_seconds
    access_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    authorization_key = Ed25519PrivateKey.generate()
    commitment_key = Ed25519PrivateKey.generate()
    if authority_state is not None:
        # Keep custody separate from the directory of handoff artifacts.
        with (authority_state / "commitment-private.pem").open("xb") as stream:
            stream.write(commitment_key.private_bytes(
                Encoding.PEM, PrivateFormat.PKCS8, NoEncryption(),
            ))
    original = matching_decision()
    principal = replace(original.principal, issuer=ISSUER)
    decision = replace(original, principal=principal, decided_at=now)

    publish(state, decision)
    SqliteProduct001CommercialApproval(
        database_path=state / "commercial.sqlite",
    ).register_grant(
        event_id="sp001-lab-grant",
        grant=replace(
            grant(), principal=principal, valid_from=now, expires_at=credential_deadline,
        ),
    )

    if revocation_order == "before-consume":
        SqliteProduct001CommercialDecisionWriter(
            database_path=state / "commercial.sqlite", clock=lambda: int(time()),
        )

    # The handoff copies commercial.sqlite alone. Flush its grant out of WAL
    # before the deliberate process exit can leave the sidecar behind.
    with closing(sqlite3.connect(state / "commercial.sqlite")) as database:
        busy, _, _ = database.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
        if busy:
            raise RuntimeError("commercial grant checkpoint incomplete")

    document = Product001DocumentaryCommitmentKey(
        organization_id=decision.document_scope.organization_id,
        source_identity=decision.document_identity,
    )
    decision_bytes = authorization_payload(decision)
    unsigned = ContextualAuthorizationV1(
        operation_id=decision.decision_id,
        decision_digest=decision_digest_from_canonical_bytes(decision_bytes),
        issuer_id=ISSUER,
        authority_sequence=1,
        materialize_deadline=commitment_deadline,
        documentary_binding=documentary_binding_from_key(document),
        signature=bytes(64),
    )
    authorization = replace(
        unsigned, signature=authorization_key.sign(authorization_signing_payload(unsigned)),
    )
    store = SqliteMvp1AuthorizationStore(
        database_path=(authority_state or state) / "authority.sqlite",
        issuer_id=ISSUER,
        public_key=authorization_key.public_key(),
    )
    context = dict(
        operation_id=decision.decision_id, decision_bytes=decision_bytes,
        documentary_key=document,
    )
    identity = dict(
        organization_id=document.organization_id,
        operation_id=decision.decision_id,
        authorization_digest=authorization_digest(authorization),
    )
    (state / "access-public.pem").write_bytes(
        access_key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo),
    )
    credential = jwt.encode(
        {
            "iss": ISSUER, "sub": principal.subject, "aud": AUDIENCE,
            "iat": now, "nbf": now, "exp": credential_deadline,
        },
        access_key, algorithm="RS256", headers={"kid": KEY_ID, "typ": "at+jwt"},
    )
    if authority_state is not None:
        (authority_state / "authorization-public.pem").write_bytes(
            authorization_key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo),
        )
        (authority_state / "recovery.json").write_text(
            json.dumps({"identity": identity, "credential": credential}), encoding="utf-8",
        )

    store.register(authorization, **context)
    revocation = dict(
        organization_id=identity["organization_id"],
        operation_id=identity["operation_id"],
        expected_digest=identity["authorization_digest"],
    )
    if revocation_order == "before-consume":
        if not store.revoke(**revocation):
            raise RuntimeError("expected first revocation to commit")
        try:
            store.consume(authorization, **context)
        except PermissionError:
            if store.recover(**revocation) is not None:
                raise RuntimeError("revoked authorization left a durable intent")
            print("Revocation before consumption: denied, no durable intent")
            return
        raise RuntimeError("revoked authorization was consumed")

    store.consume(authorization, **context)
    if revocation_order == "after-consume":
        if not store.revoke(**revocation):
            raise RuntimeError("expected first revocation to commit")
        print("Revocation after consumption: committed", flush=True)
    if interrupt:
        os._exit(INTERRUPTED_AFTER_COMMIT)
    deliver(state, store, commitment_key, identity, credential)


def deliver(state, store, commitment_key, identity, credential):
    intent = store.recover(
        organization_id=identity["organization_id"],
        operation_id=identity["operation_id"],
        expected_digest=identity["authorization_digest"],
    )
    if intent is None:
        raise RuntimeError("laboratory commitment was not recorded")
    certificate = Mvp1CommitmentIssuer(store=store, signing_key=commitment_key).issue(
        **identity,
    )
    if certificate is None:
        raise RuntimeError("laboratory commitment was not recorded")
    (state / "trust.json").write_text(json.dumps({
        "commitment_public_key_hex": commitment_key.public_key().public_bytes_raw().hex(),
        "commitments": [asdict(certificate.context)],
    }), encoding="utf-8")
    body = json.dumps({
        "decision": json.loads(intent.decision_bytes)["decision"],
        "certificate": {
            "version": 1,
            "context": asdict(certificate.context),
            "signature_b64": b64encode(certificate.signature).decode("ascii"),
        },
    })
    # curl reads the credential from stdin, away from argv and console output.
    (state / "probe.curl").write_text(
        f'url = "http://127.0.0.1:{PORT}{ROUTE}"\n'
        f'header = "Authorization: Bearer {credential}"\n'
        'header = "Content-Type: application/json"\n'
        f'data-binary = {json.dumps(body)}\n',
        encoding="utf-8",
    )
    print(f"Original materialization deadline: {certificate.context.materialize_deadline}")


def recover(state: Path) -> None:
    identity = json.loads((state / "recovery.json").read_text(encoding="utf-8"))
    private_key = load_pem_private_key(
        (state / "commitment-private.pem").read_bytes(), password=None,
    )
    public_key = load_pem_public_key((state / "authorization-public.pem").read_bytes())
    store = SqliteMvp1AuthorizationStore(
        database_path=state / "authority.sqlite",
        issuer_id=ISSUER, public_key=public_key, read_only=True,
    )
    deliver(state / "handoff", store, private_key, identity["identity"], identity["credential"])


def serve(
    state: Path, commercial_uid: int, *, enable_receipts=False, interrupt_before_receipt=False,
) -> None:
    key = load_pem_public_key((state / "access-public.pem").read_bytes())
    service = compose_product001_commercial_approval(
        issuer=ISSUER,
        audience=AUDIENCE,
        key_resolver=ConfiguredAccessTokenKeys(issuer=ISSUER, public_keys={KEY_ID: key}),
        max_lifetime_seconds=CREDENTIAL_TTL_SECONDS,
        max_token_bytes=8192,
        database_path=state / "commercial.sqlite",
        documentary_storage_root=state / "documents",
        clock=lambda: int(time()),
    )
    receipts = None
    if enable_receipts:
        receipts = GateReceiptConfiguration(
            signing_key_path=state.parent / "receipt-key.raw",
            database_path=state / "commercial.sqlite",
            gate_id="sp001-gate-lab",
            authority_issuer_id=ISSUER,
        )

    def interrupt():
        os._exit(76)

    app = create_product001_mvp1_deployed_gate(
        authenticated_service=service,
        trust_configuration_path=state / "trust.json",
        commercial_uid=commercial_uid,
        receipt_configuration=receipts,
        after_commit=interrupt if interrupt_before_receipt else None,
    )
    uvicorn.run(app, host="127.0.0.1", port=PORT, access_log=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("provision", "issue", "recover", "serve"))
    parser.add_argument("state", type=Path)
    parser.add_argument("--commercial-uid", type=int)
    parser.add_argument("--authority-uid", type=int)
    parser.add_argument("--interrupt-after-commit", action="store_true")
    parser.add_argument("--commitment-ttl-seconds", type=int)
    parser.add_argument("--revocation-order", choices=("before-consume", "after-consume"))
    parser.add_argument("--enable-receipts", action="store_true")
    parser.add_argument("--interrupt-before-receipt", action="store_true")
    args = parser.parse_args()
    if args.enable_receipts and args.action != "serve":
        parser.error("--enable-receipts requires serve")
    if args.interrupt_before_receipt and not args.enable_receipts:
        parser.error("--interrupt-before-receipt requires --enable-receipts")
    if args.revocation_order is not None and args.action != "issue":
        parser.error("--revocation-order requires issue")
    if args.revocation_order == "before-consume" and args.interrupt_after_commit:
        parser.error("revocation before consumption has no consumption commit to interrupt")
    if args.commitment_ttl_seconds is not None:
        if args.action != "issue":
            parser.error("--commitment-ttl-seconds requires issue")
        if not 1 <= args.commitment_ttl_seconds < CREDENTIAL_TTL_SECONDS:
            parser.error("commitment TTL must be shorter than the credential lifetime")
    if args.interrupt_after_commit and args.action != "issue":
        parser.error("--interrupt-after-commit requires issue")
    os.umask(0o077)
    if not args.state.is_absolute() or os.geteuid() == 0:
        parser.error("an absolute state path and unprivileged Gate account are required")
    if args.action == "provision":
        provision(args.state)
    elif args.action in ("issue", "recover"):
        if args.authority_uid != os.geteuid():
            parser.error("issue and recover require the configured authority UID")
        if args.action == "recover":
            recover(args.state)
        else:
            args.state.mkdir(mode=0o700)
            provision(
                args.state / "handoff", authority_state=args.state,
                interrupt=args.interrupt_after_commit,
                commitment_ttl_seconds=args.commitment_ttl_seconds or CREDENTIAL_TTL_SECONDS,
                revocation_order=args.revocation_order,
            )
    else:
        if args.commercial_uid is None:
            parser.error("--commercial-uid is required for serve")
        serve(
            args.state, args.commercial_uid, enable_receipts=args.enable_receipts,
            interrupt_before_receipt=args.interrupt_before_receipt,
        )


if __name__ == "__main__":
    main()
