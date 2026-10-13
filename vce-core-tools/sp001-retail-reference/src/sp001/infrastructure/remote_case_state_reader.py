import http.client
import json
import math
import socket
import ssl
from urllib.parse import urlencode, urlsplit

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_resource_link import CaseResourceLink
from sp001.contracts.case_state_read_result import (
    BackendUnavailable,
    CaseStateReadResult,
    Found,
    InvalidResponse,
    NotFound,
    RequestRejected,
    TransportUnavailable,
)


CONTRACT_VERSION = "sp001.case-state.v1"


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _constant(value):
    raise ValueError("nonstandard JSON constant")


def _keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError("invalid object fields")


def classify_case_state_response(
    *,
    case_id: str,
    status_code: int,
    content_type: str,
    body: bytes,
) -> CaseStateReadResult:
    if status_code == 429 or 500 <= status_code <= 599:
        return BackendUnavailable(status_code)
    if 400 <= status_code <= 499 and status_code != 404:
        return RequestRejected(status_code, "http_request_rejected")
    if status_code not in (200, 404):
        return InvalidResponse("unexpected_http_status")
    if content_type.split(";", 1)[0].strip().lower() != "application/json":
        return InvalidResponse("invalid_content_type")

    try:
        payload = json.loads(
            body.decode("utf-8"),
            object_pairs_hook=_object,
            parse_constant=_constant,
        )
        expected = {"contract_version", "code", "case_id"}
        if status_code == 200:
            expected.add("state")
        _keys(payload, expected)
        if payload["contract_version"] != CONTRACT_VERSION:
            raise ValueError("unsupported contract version")
        if payload["case_id"] != case_id:
            raise ValueError("case identity mismatch")
        if status_code == 404:
            if payload["code"] != "CASE_NOT_FOUND":
                raise ValueError("404 without explicit business absence")
            return NotFound(case_id)

        if payload["code"] != "CASE_FOUND":
            raise ValueError("unexpected domain code")
        value = payload["state"]
        _keys(value, {
            "case_id", "objective_id", "scope", "phase",
            "revision", "resource_links",
        })
        if value["case_id"] != case_id:
            raise ValueError("state identity mismatch")
        if not isinstance(value["phase"], str):
            raise TypeError("phase must be a string")
        if not isinstance(value["resource_links"], list):
            raise TypeError("resource_links must be an array")
        links = []
        for link in value["resource_links"]:
            _keys(link, {"relationship", "resource_type", "resource_id"})
            links.append(CaseResourceLink(**link))
        state = CaseAuthoritativeState(
            case_id=value["case_id"],
            objective_id=value["objective_id"],
            scope=value["scope"],
            phase=CaseLifecyclePhase(value["phase"]),
            revision=value["revision"],
            resource_links=tuple(links),
        )
        return Found(state)
    except (UnicodeError, ValueError, TypeError, RecursionError):
        return InvalidResponse("invalid_case_state_contract")


class RemoteCaseStateReader:
    """HTTPS reader with certificate validation and no redirects or retries."""

    def __init__(
        self,
        *,
        endpoint: str,
        timeout_seconds: float,
        max_response_bytes: int,
        ca_file: str | None = None,
    ) -> None:
        if not isinstance(endpoint, str):
            raise TypeError("endpoint must be a string")
        parts = urlsplit(endpoint)
        if (
            parts.scheme != "https"
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
            or parts.query
            or parts.fragment
            or parts.path != "/v1/case-state"
        ):
            raise ValueError("endpoint must be an HTTPS case-state URL")
        if any(ord(char) <= 32 or ord(char) == 127 for char in endpoint):
            raise ValueError("endpoint contains invalid characters")
        if (
            isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(timeout_seconds)
            or timeout_seconds <= 0
        ):
            raise ValueError("timeout_seconds must be finite and positive")
        if (
            isinstance(max_response_bytes, bool)
            or not isinstance(max_response_bytes, int)
            or max_response_bytes <= 0
        ):
            raise ValueError("max_response_bytes must be a positive integer")
        self._host = parts.hostname
        self._port = parts.port
        self._path = parts.path
        self._timeout = timeout_seconds
        self._limit = max_response_bytes
        if ca_file is not None:
            if not isinstance(ca_file, str):
                raise TypeError("ca_file must be a string or None")
            if not ca_file.strip():
                raise ValueError("ca_file must not be empty")
        self._tls = ssl.create_default_context(cafile=ca_file)

    def read(self, *, case_id: str) -> CaseStateReadResult:
        if not isinstance(case_id, str):
            raise TypeError("case_id must be a string")
        if not case_id.strip():
            raise ValueError("case_id must not be empty")
        connection = http.client.HTTPSConnection(
            self._host,
            port=self._port,
            timeout=self._timeout,
            context=self._tls,
        )
        try:
            connection.request(
                "GET",
                self._path + "?" + urlencode({"case_id": case_id}),
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "identity",
                },
            )
            response = connection.getresponse()
            status = response.status
            # Status-only failures do not require trusting or reading a body.
            if status == 429 or 500 <= status <= 599:
                return BackendUnavailable(status)
            if 400 <= status <= 499 and status != 404:
                return RequestRejected(status, "http_request_rejected")
            if status not in (200, 404):
                return InvalidResponse("unexpected_http_status")
            if response.getheader("Content-Encoding", "identity") != "identity":
                return InvalidResponse("unsupported_content_encoding")
            body = response.read(self._limit + 1)
            if len(body) > self._limit:
                return InvalidResponse("response_size_limit_exceeded")
            return classify_case_state_response(
                case_id=case_id,
                status_code=status,
                content_type=response.getheader("Content-Type", ""),
                body=body,
            )
        except ssl.SSLCertVerificationError:
            return InvalidResponse("tls_peer_verification_failed")
        except (socket.timeout, ConnectionError, socket.gaierror):
            return TransportUnavailable("connection_unavailable")
        except (ssl.SSLError, http.client.HTTPException):
            return InvalidResponse("invalid_transport_response")
        except OSError:
            return TransportUnavailable("transport_os_error")
        finally:
            connection.close()
