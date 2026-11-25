"""Startup composition for the PRODUCT-001 MVP1 certificate Gate on POSIX."""

from collections.abc import Callable
from dataclasses import dataclass, fields
import os
from pathlib import Path
import re
import stat
from time import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from fastapi import FastAPI

from sp001.contracts.product001_mvp1_commitment_certificate import CommitmentContextV1
from sp001.infrastructure.product001_mvp1_http_host import create_product001_mvp1_http_app
from sp001.infrastructure.product001_mvp1_http_json_parser import (
    MAX_PRODUCT001_MVP1_BODY_BYTES,
    parse_product001_mvp1_json_body,
)
from sp001.infrastructure.product001_mvp1_protected_composition import (
    compose_product001_mvp1_protected_approval,
)
from sp001.services.authenticated_product001_commercial_approval import (
    AuthenticatedProduct001CommercialApproval,
)
from sp001.services.product001_mvp1_execution_gate import MVP1CommitmentAdmission
from sp001.services.product001_mvp1_commercial_receipt_issuer import Mvp1CommercialReceiptIssuer


@dataclass(frozen=True, slots=True)
class GateReceiptConfiguration:
    signing_key_path: Path
    database_path: Path
    gate_id: str
    authority_issuer_id: str


def _require_trusted_permissions(fd, *, gate_uid, expected_type):
    info = os.fstat(fd)
    if (
        not expected_type(info.st_mode)
        or info.st_uid not in (0, gate_uid)
        or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
    ):
        raise PermissionError("unsafe Gate trust configuration ownership or permissions")


def _read_trusted_file(path: Path, *, gate_uid: int, private_key: bool = False) -> bytes:
    if path.anchor != "/" or len(path.parts) < 2 or ".." in path.parts:
        raise ValueError("absolute Gate trust configuration path required")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory = os.open(path.anchor, directory_flags)
    try:
        _require_trusted_permissions(directory, gate_uid=gate_uid, expected_type=stat.S_ISDIR)
        for name in path.parts[1:-1]:
            child = os.open(name, directory_flags, dir_fd=directory)
            os.close(directory)
            directory = child
            _require_trusted_permissions(
                directory, gate_uid=gate_uid, expected_type=stat.S_ISDIR,
            )
        fd = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory,
        )
        try:
            _require_trusted_permissions(fd, gate_uid=gate_uid, expected_type=stat.S_ISREG)
            if private_key and stat.S_IMODE(os.fstat(fd).st_mode) != 0o600:
                raise PermissionError("Gate receipt key must have mode 0600")
            limit = 33 if private_key else MAX_PRODUCT001_MVP1_BODY_BYTES + 1
            with os.fdopen(fd, "rb", closefd=False) as stream:
                return stream.read(limit)
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def _read_trust_configuration(path: Path, *, gate_uid: int) -> dict:
    return parse_product001_mvp1_json_body(_read_trusted_file(path, gate_uid=gate_uid))


def create_product001_mvp1_deployed_gate(
    *,
    authenticated_service: AuthenticatedProduct001CommercialApproval,
    trust_configuration_path: Path,
    commercial_uid: int,
    receipt_configuration: GateReceiptConfiguration | None = None,
    after_commit: Callable[[], None] | None = None,
) -> FastAPI:
    """Load a fixed trust configuration before enabling the certificate route.

    The supervisor supplies the service, path and commercial account identity.
    This checks POSIX owner and mode bits at startup. The deployment must
    independently establish the account mapping, ACLs and process isolation.
    """
    gate_uid = os.geteuid()
    if (
        gate_uid == 0
        or type(commercial_uid) is not int
        or commercial_uid <= 0
        or commercial_uid == gate_uid
    ):
        raise PermissionError("Gate and commercial process require distinct unprivileged accounts")

    config = _read_trust_configuration(Path(trust_configuration_path), gate_uid=gate_uid)
    if set(config) != {"commitment_public_key_hex", "commitments"}:
        raise ValueError("invalid Gate trust configuration fields")
    key_hex = config["commitment_public_key_hex"]
    if type(key_hex) is not str or re.fullmatch(r"[0-9a-f]{64}", key_hex) is None:
        raise ValueError("invalid Gate commitment public key")
    key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(key_hex))

    entries = config["commitments"]
    if type(entries) is not list or not entries:
        raise ValueError("Gate requires trusted commitment contexts")
    expected_fields = {field.name for field in fields(CommitmentContextV1)}
    contexts = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != expected_fields:
            raise ValueError("invalid trusted commitment context fields")
        context = CommitmentContextV1(**entry)
        identity = (context.organization_id, context.operation_id)
        if identity in contexts:
            raise ValueError("duplicate trusted commitment identity")
        contexts[identity] = context

    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated_service,
        commitment_admission=MVP1CommitmentAdmission(
            public_key=key,
            resolve_context=lambda org, operation: contexts.get((org, operation)),
            clock=lambda: int(time()),
        ),
    )
    issuer = None
    if receipt_configuration is not None:
        issuer = Mvp1CommercialReceiptIssuer(
            database_path=receipt_configuration.database_path,
            gate_id=receipt_configuration.gate_id,
            signing_key=Ed25519PrivateKey.from_private_bytes(_read_trusted_file(
                receipt_configuration.signing_key_path, gate_uid=gate_uid, private_key=True,
            )),
            trusted_issuer_id=receipt_configuration.authority_issuer_id,
            trusted_authority_key=key,
        )
    return create_product001_mvp1_http_app(
        protected_service=protected, enable_commitment_route=True,
        receipt_issuer=issuer, after_commit=after_commit,
    )
