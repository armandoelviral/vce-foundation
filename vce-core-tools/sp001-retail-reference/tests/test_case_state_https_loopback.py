import asyncio
from datetime import datetime, timedelta, timezone
import ipaddress
import socket
import threading
import time

import pytest
import uvicorn
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_state_read_result import Found, InvalidResponse, NotFound
from sp001.infrastructure.case_state_http_host import create_case_state_app
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader
from sp001.services.case_state_subscription import CaseStateSubscription
from sp001.services.case_state_reconciliation import ViewStatus


def certificates(directory):
    now = datetime.now(timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "SP001 temporary test CA"),
    ])
    ca = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .add_extension(x509.KeyUsage(
            digital_signature=True, content_commitment=False,
            key_encipherment=False, data_encipherment=False,
            key_agreement=False, key_cert_sign=True, crl_sign=True,
            encipher_only=False, decipher_only=False,
        ), critical=True)
        .sign(ca_key, hashes.SHA256())
    )
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(ca_name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .add_extension(x509.ExtendedKeyUsage([
            x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
        ]), critical=False)
        .sign(ca_key, hashes.SHA256())
    )
    ca_path = directory / "ca.pem"
    cert_path = directory / "server.pem"
    key_path = directory / "server-key.pem"
    ca_path.write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    cert_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    key_path.chmod(0o600)
    return ca_path, cert_path, key_path


class Reader:
    def __init__(self):
        self.calls = []
        self.state = CaseAuthoritativeState(
            case_id="CASE-001",
            objective_id="OBJ-001",
            scope="STORE-001",
            phase=CaseLifecyclePhase.CASE_OPENED,
            revision=8,
            resource_links=(),
        )

    def read(self, *, case_id):
        self.calls.append(case_id)
        if case_id == self.state.case_id:
            return Found(self.state)
        return NotFound(case_id)


@pytest.fixture
def https_host(tmp_path):
    ca, certificate, key = certificates(tmp_path)
    reader = Reader()
    app = create_case_state_app(
        reader=reader,
        authorize=lambda request, case_id: True,
    )
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        ssl_certfile=str(certificate),
        ssl_keyfile=str(key),
        lifespan="off",
        loop="asyncio",
        access_log=False,
        log_level="critical",
        timeout_graceful_shutdown=1,
    )
    server = uvicorn.Server(config)
    failures = []

    def run():
        try:
            asyncio.run(server.serve(sockets=[listener]))
        except BaseException as error:
            failures.append(error)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 5
        while not server.started and thread.is_alive():
            if time.monotonic() >= deadline:
                pytest.fail("HTTPS server did not start within test deadline")
            time.sleep(0.01)
        if failures:
            raise failures[0]
        if not server.started:
            pytest.fail("HTTPS server stopped before startup")
        yield port, ca, reader
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        if thread.is_alive():
            pytest.fail("HTTPS server did not stop within test deadline")


def remote(port, ca=None, hostname="localhost"):
    return RemoteCaseStateReader(
        endpoint=f"https://{hostname}:{port}/v1/cases/{{caseId}}/state",
        timeout_seconds=2,
        max_response_bytes=4096,
        ca_file=str(ca) if ca is not None else None,
    )


def test_trusted_https_round_trip_reaches_reconciled_view(https_host):
    port, ca, host_reader = https_host
    subscription = CaseStateSubscription(
        reader=remote(port, ca), case_id="CASE-001"
    )
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state == host_reader.state
    assert host_reader.calls == ["CASE-001"]


def test_trusted_https_business_absence_is_explicit(https_host):
    port, ca, host_reader = https_host
    subscription = CaseStateSubscription(
        reader=remote(port, ca), case_id="MISSING"
    )
    view = subscription.refresh()
    assert view.status is ViewStatus.NOT_FOUND
    assert view.last_valid_state is None
    assert host_reader.calls == ["MISSING"]


def test_untrusted_ca_rejected_before_domain_read(https_host):
    port, ca, host_reader = https_host
    result = remote(port).read(case_id="CASE-001")
    assert result == InvalidResponse("tls_peer_verification_failed")
    assert host_reader.calls == []


def test_trusted_ca_wrong_hostname_rejected_before_domain_read(https_host):
    port, ca, host_reader = https_host
    # Certificate has DNS localhost only, no IP subject alternative name.
    result = remote(port, ca, hostname="127.0.0.1").read(case_id="CASE-001")
    assert result == InvalidResponse("tls_peer_verification_failed")
    assert host_reader.calls == []


def test_tls_failure_preserves_previous_valid_view(https_host):
    port, ca, host_reader = https_host
    good = remote(port, ca)
    bad = remote(port)

    class SwitchingReader:
        def __init__(self):
            self.current = good

        def read(self, *, case_id):
            return self.current.read(case_id=case_id)

    reader = SwitchingReader()
    subscription = CaseStateSubscription(reader=reader, case_id="CASE-001")
    original = subscription.refresh().last_valid_state
    reader.current = bad
    view = subscription.refresh()
    assert view.status is ViewStatus.INVALID_RESPONSE
    assert view.last_valid_state is original
    assert host_reader.calls == ["CASE-001"]
