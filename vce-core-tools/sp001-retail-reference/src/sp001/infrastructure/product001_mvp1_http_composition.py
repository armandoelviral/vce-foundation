"""PRODUCT-001 MVP1: isolated HTTP input composition.

This module only reads, parses and decodes untrusted input.

It does not verify signatures, authorize operations,
invoke the execution Gate, persist state or expose HTTP routes.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from sp001.infrastructure.product001_mvp1_http_bounded_body import (
    read_product001_mvp1_bounded_body,
)
from sp001.infrastructure.product001_mvp1_http_json_parser import (
    parse_product001_mvp1_json_body,
)
from sp001.infrastructure.product001_mvp1_http_codec import (
    decode_product001_mvp1_decision,
    decode_product001_mvp1_commitment_certificate,
    decode_product001_mvp1_authorization,
)


async def read_product001_mvp1_decision(
    receive: Callable[[], Awaitable[dict[str, Any]]],
    *,
    content_length: str | None,
):
    """Decode an untrusted decision without granting authority."""
    body = await read_product001_mvp1_bounded_body(
        receive,
        content_length=content_length,
    )
    payload = parse_product001_mvp1_json_body(body)
    return decode_product001_mvp1_decision(payload)


async def read_product001_mvp1_authorization(
    receive: Callable[[], Awaitable[dict[str, Any]]],
    *,
    content_length: str | None,
):
    """Decode signature bytes without cryptographic verification."""
    body = await read_product001_mvp1_bounded_body(
        receive,
        content_length=content_length,
    )
    payload = parse_product001_mvp1_json_body(body)
    return decode_product001_mvp1_authorization(payload)



async def read_product001_mvp1_commitment_request(
    receive: Callable[[], Awaitable[dict[str, Any]]],
    *,
    content_length: str | None,
):
    """Decode the decision and certificate from one bounded JSON envelope."""
    body = await read_product001_mvp1_bounded_body(
        receive, content_length=content_length,
    )
    payload = parse_product001_mvp1_json_body(body)
    if set(payload) != {"decision", "certificate"}:
        raise ValueError("invalid commitment request fields")
    return (
        decode_product001_mvp1_decision(payload["decision"]),
        decode_product001_mvp1_commitment_certificate(payload["certificate"]),
    )
