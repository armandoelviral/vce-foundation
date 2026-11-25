"""Opt-in intelligence pilot for the protected VCE Gate."""

import asyncio
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import re
import sqlite3
from time import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import FastAPI, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from sp001.contracts.federated_issuance_context import ValidatedFederatedIssuanceContext
from sp001.infrastructure.product001_mvp1_http_bounded_body import (
    read_product001_mvp1_bounded_body,
)
from sp001.infrastructure.product001_mvp1_http_json_parser import (
    parse_product001_mvp1_json_body,
)

_DOMAIN = "VCE/INTELLIGENCE/LAB/VERSION-CHECK/V1"
_PATH = "/laboratory/vce/intelligence/version-checks"
_DEVICES = {"EQ-01", "EQ-02", "EQ-03"}


class AlreadyConsumed(ValueError):
    pass


def _canonical(value):
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("ascii")


class IntelligenceLabGate:
    """Bind one configured signer to an authenticated principal and a local store."""

    def __init__(self, *, database_path, authenticator, audience, trust, clock=lambda: int(time())):
        if set(trust) != {"signer_id", "issuer", "subject", "public_key_hex"}:
            raise ValueError("invalid intelligence trust configuration")
        if any(type(value) is not str or not value.strip() for value in trust.values()):
            raise ValueError("invalid intelligence signer or principal")
        if re.fullmatch(r"[0-9a-f]{64}", trust["public_key_hex"]) is None:
            raise ValueError("invalid intelligence public key")
        self._key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(trust["public_key_hex"]))
        self._signer = trust["signer_id"]
        self._principal = (trust["issuer"], trust["subject"])
        self._authenticator = authenticator
        self._audience = audience
        self._clock = clock
        self._path = Path(database_path)
        with closing(self._connect()) as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS intelligence_consumption (
                    operation TEXT PRIMARY KEY,
                    authorization_digest TEXT NOT NULL,
                    signer_id TEXT NOT NULL,
                    principal_issuer TEXT NOT NULL,
                    principal_subject TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS intelligence_observations (
                    operation TEXT NOT NULL REFERENCES intelligence_consumption(operation),
                    device TEXT NOT NULL,
                    evidence_id TEXT NOT NULL,
                    observed_version TEXT NOT NULL,
                    affected INTEGER NOT NULL CHECK (affected IN (0, 1)),
                    PRIMARY KEY (operation, device)
                );
            """)

    def _connect(self):
        db = sqlite3.connect(self._path)
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA synchronous=FULL")
        except Exception:
            db.close()
            raise
        return db

    def submit(self, *, credential, request):
        context = self._authenticator.authenticate(credential=credential)
        if not isinstance(context, ValidatedFederatedIssuanceContext) or (
            context.principal.issuer, context.principal.subject
        ) != self._principal:
            raise PermissionError("authenticated principal is not the configured signer")

        if type(request) is not dict or set(request) != {"revision", "equipos", "autorizacion"}:
            raise ValueError("invalid intelligence request")
        review, devices, envelope = request["revision"], request["equipos"], request["autorizacion"]
        if (
            type(review) is not dict or review.get("case_id") != "VCE-INTEL-001"
            or review.get("mode") != "simulado" or type(review.get("revision")) is not int
            or review["revision"] < 1 or type(review.get("scope")) is not dict
            or type(review.get("configured_sources")) is not list or not review["configured_sources"]
            or type(devices) is not list or not devices
            or any(type(device) is not str or device not in _DEVICES for device in devices)
            or len(set(devices)) != len(devices)
            or type(envelope) is not dict or set(envelope) != {"statement", "signature_hex"}
            or type(envelope["statement"]) is not dict
            or type(envelope["signature_hex"]) is not str
            or re.fullmatch(r"[0-9a-f]{128}", envelope["signature_hex"]) is None
        ):
            raise ValueError("invalid intelligence evidence")

        statement = envelope["statement"]
        signature = bytes.fromhex(envelope["signature_hex"])
        signed = _canonical(statement)
        try:
            self._key.verify(signature, signed)
        except InvalidSignature as error:
            raise PermissionError("invalid intelligence authorization signature") from error
        issued, expires = statement.get("issued_at"), statement.get("expires_at")
        if type(issued) is not int or type(expires) is not int or not 1 <= expires - issued <= 600:
            raise PermissionError("invalid authorization lifetime")

        snapshot = {key: value for key, value in review.items() if key not in {"authorization", "observations"}}
        review_digest = sha256(_canonical(snapshot)).hexdigest()
        ordered = sorted(devices)
        expected = {
            "domain": _DOMAIN, "case_id": review["case_id"], "revision": review["revision"],
            "review_sha256": review_digest, "action": "comprobar versiones", "mode": "simulado",
            "devices": ordered, "signer_id": self._signer, "issued_at": issued, "expires_at": expires,
        }
        if signed != _canonical(expected):
            raise PermissionError("authorization does not match intelligence request")

        operation = sha256(_canonical([_DOMAIN, review["case_id"], review["revision"]])).hexdigest()
        with closing(self._connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            now = self._clock()
            context.require_valid(expected_audience=self._audience, at_time=now)
            if not issued <= now < expires:
                raise PermissionError("intelligence authorization expired")
            if db.execute(
                "SELECT 1 FROM intelligence_consumption WHERE operation = ?", (operation,),
            ).fetchone():
                raise AlreadyConsumed("revision already consumed")
            db.execute(
                "INSERT INTO intelligence_consumption VALUES (?, ?, ?, ?, ?)",
                (operation, sha256(signed + signature).hexdigest(), self._signer, *self._principal),
            )
            # The simulation has no external effects. Its rows and the consumption
            # marker commit together, or both roll back.
            observations = [
                {"device": device, "evidence_id": "SIM-OBS-" + device.removeprefix("EQ-"),
                 "version": "1.0 ficticia", "affected": True}
                for device in ordered
            ]
            db.executemany(
                "INSERT INTO intelligence_observations VALUES (?, ?, ?, ?, ?)",
                ((operation, row["device"], row["evidence_id"], row["version"], 1)
                 for row in observations),
            )
        return {"operation": operation, "mode": "simulado", "observations": observations}


def mount_intelligence_lab(app: FastAPI, gate: IntelligenceLabGate) -> None:
    @app.post(_PATH)
    async def version_check(request: Request):
        credentials = request.headers.getlist("authorization")
        if len(credentials) != 1:
            raise HTTPException(401, "Bearer credential required")
        scheme, _, credential = credentials[0].partition(" ")
        if scheme.lower() != "bearer" or not credential or any(
            char.isspace() or char == "," for char in credential
        ):
            raise HTTPException(401, "Bearer credential required")
        lengths = request.headers.getlist("content-length")
        if len(lengths) > 1:
            raise HTTPException(400, "Invalid Content-Length")
        try:
            async with asyncio.timeout(5):
                body = await read_product001_mvp1_bounded_body(
                    request.receive, content_length=lengths[0] if lengths else None,
                )
            payload = parse_product001_mvp1_json_body(body)
            return await run_in_threadpool(gate.submit, credential=credential, request=payload)
        except TimeoutError as error:
            raise HTTPException(408, "Request body timeout") from error
        except PermissionError as error:
            raise HTTPException(403, "Intelligence authorization denied") from error
        except AlreadyConsumed as error:
            raise HTTPException(409, "Intelligence revision already consumed") from error
        except (TypeError, ValueError) as error:
            raise HTTPException(400, "Invalid intelligence request") from error
        except sqlite3.Error as error:
            raise HTTPException(503, "Intelligence register unavailable") from error
